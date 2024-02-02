from pydantic import BaseModel, Field
from pydantic.types import date

from nashafirma_fastapi.schemas.users import UserFromOrder


class OrderModel(BaseModel):
    done: bool = Field(False)


class OrderFromItem(BaseModel):
    created_at: date

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user: UserFromOrder
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class OrderCreate(OrderModel):
    pass
