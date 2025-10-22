# schemas.py
# Isse API data ko validate karte h

from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    product: str
    phone: str | None = None
    email: str | None = None
    quantity: int
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True
