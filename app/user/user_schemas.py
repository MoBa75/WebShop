from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    This schema is typically used when a user registers or is created by an admin.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (EmailStr): The user's unique email address.
        company (Optional[str]): The company the user is affiliated with (optional).
        is_admin (Optional[bool]): Whether the user is an admin. Defaults to False.
        birth_date (Optional[date]): The user's date of birth, must not be in the future or unrealistically old.
    """
    first_name: str
    last_name: str
    email: EmailStr
    company: Optional[str] = None
    is_admin: Optional[bool] = False
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
    """
    Schema for updating an existing user.
    All fields are optional to allow partial updates.

    Attributes:
        first_name (Optional[str]): The user's first name.
        last_name (Optional[str]): The user's last name.
        email (Optional[EmailStr]): The user's email address.
        company (Optional[str]): The user's company.
        is_admin (Optional[bool]): Whether the user is an admin.
        birth_date (Optional[date]): The user's birth date, validated against future/past logic.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
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
