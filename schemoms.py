from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class FundRequest(BaseModel):
    amt: float

class PayRequest(BaseModel):
    to: str
    amt: float

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class BuyRequest(BaseModel):
    product_id: int
