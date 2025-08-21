from pydantic import BaseModel, EmailStr
from models.portalSchema import Asset
from typing import List

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    assets: List[Asset]
    virtualBalance: int