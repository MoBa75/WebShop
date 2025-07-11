from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date
from typing import Optional, List


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
    zip_code: int
    city: str
    is_admin: Optional[bool] = False
    company: Optional[str] = None
    birth_date: Optional[date] = Field(default=None)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, birth_date_value: Optional[date]):
        if birth_date_value:
            today = date.today()
            if birth_date_value > today:
                raise ValueError("Birth date cannot be in the future")
            if birth_date_value < today.replace(year=today.year - 95):
                raise ValueError("Birth date is too far in the past")
        return birth_date_value


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[int] = None
    city: Optional[str] = None
    company: Optional[str] = None
    is_admin: Optional[bool] = None
    birth_date: Optional[date] = Field(default=None)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, birth_date_value: Optional[date]):
        if birth_date_value:
            today = date.today()
            if birth_date_value > today:
                raise ValueError("Birth date cannot be in the future")
            if birth_date_value < today.replace(year=today.year - 95):
                raise ValueError("Birth date is too far in the past")
        return birth_date_value


class ProductCreate(BaseModel):
    name: str
    unit: str
    price: float = Field(..., ge=0, description="Price must be non-negative")
    description: str
    stock: int = Field(..., ge=0, description="Stock must be non-negative")


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = Field(None, ge=0, description="Price must be non-negative")
    description: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0, description="Stock must be non-negative")


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
