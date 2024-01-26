from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.types import datetime


class UserModel(BaseModel):
    username: str = Field(max_length=150)
    email: EmailStr
    password: str = Field(max_length=350)
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    phone: str = Field(max_length=25)


class UserResponse(UserModel):
    id: int
    username: str
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    # avatar: str | None
    confirmed: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserFromOrder(UserModel):
    id: int
    username: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    phone: str | None


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
