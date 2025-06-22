from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db import SessionLocal
import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_user(db, credentials.username)
    if user is None or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def hash_password(password: str):
    return pwd_context.hash(password)
