from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator


class InProduct(BaseModel):
    product: str = Field(max_length=50)
    price: float = Field(0, ge=0, le=2500)


class OutProduct(InProduct):
    id: int = Field(1, gt=0)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
