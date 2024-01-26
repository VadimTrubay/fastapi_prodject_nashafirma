from datetime import datetime, date
from pydantic.types import date

from pydantic import BaseModel, Field

from ..schemas.users import UserFromOrder


class OrderModel(BaseModel):
    done: bool = Field(False)



class OrderResponse(OrderModel):
    id: int
    user: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class OrderCreate(OrderModel):
    pass
