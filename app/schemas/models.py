from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SizeQuantity(BaseModel):
    size: str
    quantity: int


class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]


class ProductOut(BaseModel):
    id: str
    name: str
    price: float


class OrderItem(BaseModel):
    productId: str
    qty: int


class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]


class ProductDetails(BaseModel):
    id: str
    name: str
    qty: int


class OrderOut(BaseModel):
    id: str
    items: List[ProductDetails]
    total: float
