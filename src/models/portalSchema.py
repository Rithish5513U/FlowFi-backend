from pydantic import BaseModel

class Asset(BaseModel):
    symbol: str
    price: int
    quantity: int