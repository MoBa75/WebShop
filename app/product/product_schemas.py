from pydantic import BaseModel, Field
from typing import Optional


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
