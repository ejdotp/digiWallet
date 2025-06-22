from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from db import Base, engine
from auth import hash_password, authenticate, get_db
from sqlalchemy.orm import Session
import schemoms, models
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", status_code=201)
def register(user: schemoms.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered"}

@app.post("/fund")
def fund_account(data: schemoms.FundRequest, user: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    user.balance += data.amt
    txn = models.Transaction(user_id=user.id, kind="credit", amt=data.amt, updated_bal=user.balance)
    db.add(txn)
    db.commit()
    return {"balance": user.balance}

@app.post("/pay")
def pay_user(data: schemoms.PayRequest, sender: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    receiver = db.query(models.User).filter_by(username=data.to).first()
    if not receiver:
        raise HTTPException(status_code=400, detail="Recipient not found")
    if sender.balance < data.amt:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    sender.balance -= data.amt
    receiver.balance += data.amt
    db.add_all([
        models.Transaction(user_id=sender.id, kind="debit", amt=data.amt, updated_bal=sender.balance),
        models.Transaction(user_id=receiver.id, kind="credit", amt=data.amt, updated_bal=receiver.balance)
    ])
    db.commit()
    return {"balance": sender.balance}

@app.get("/bal")
def get_balance(currency: str = "INR", user: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    if currency == "INR":
        return {"balance": user.balance, "currency": "INR"}
    res = requests.get("https://api.currencyapi.com/v3/latest", params={
        "apikey": "cur_live_VS0KBDjtUHoM0g9KUsYidaTLWC0ukJ4rL5GkUZU8", "base_currency": "INR"
    }).json()
    rate = res["data"][currency]["value"]
    return {"balance": user.balance * rate, "currency": currency}

@app.get("/stmt")
def get_statement(user: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    txns = db.query(models.Transaction)\
        .filter_by(user_id=user.id)\
        .order_by(models.Transaction.timestamp.desc()).all()

    result = []
    for txn in txns:
        result.append({
            "kind": txn.kind,
            "amt": txn.amt,
            "updated_bal": txn.updated_bal,
            "timestamp": txn.timestamp.isoformat()
        })
    return result

@app.post("/product", status_code=201)
def add_product(data: schemoms.ProductCreate, user: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    product = models.Product(
        name=data.name,
        price=data.price,
        description=data.description
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"id": product.id, "message": "Product added"}

@app.get("/product")
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description
        }
        for p in products
    ]

@app.post("/buy")
def buy_product(data: schemoms.BuyRequest, user: models.User = Depends(authenticate), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter_by(id=data.product_id).first()
    if not product or user.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient balance or invalid product")

    user.balance -= product.price
    txn = models.Transaction(
        user_id=user.id,
        kind="debit",
        amt=product.price,
        updated_bal=user.balance
    )
    db.add(txn)
    db.commit()
    return {"message": "Product purchased", "balance": user.balance}
