from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date
from typing import Optional, List



class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    status: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# New schemas for cart handling

class CartAddItem(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")


class CartUpdateItem(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")


class CartRemoveItem(BaseModel):
    user_id: int
    product_id: int


class CartCheckout(BaseModel):
    user_id: int


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    order_id: int
    items: List[CartItemResponse]
