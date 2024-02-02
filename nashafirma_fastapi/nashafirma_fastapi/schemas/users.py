from pydantic import BaseModel, Field, EmailStr
from pydantic.types import date


class UserModel(BaseModel):
    username: str = Field(max_length=150)
    email: EmailStr
    password: str = Field(max_length=350)
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    phone: str = Field(max_length=25)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    # password: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar: str | None
    confirmed: bool
    is_superuser: bool
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class UserFromOrder(BaseModel):
    username: str

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
