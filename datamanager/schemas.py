from pydantic import BaseModel, EmailStr
from typing import Optional

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


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[int] = None
    city: Optional[str] = None
    company: Optional[str] = None
    is_admin: Optional[bool] = None
