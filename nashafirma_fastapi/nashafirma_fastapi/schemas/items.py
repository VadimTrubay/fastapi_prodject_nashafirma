from datetime import datetime

from pydantic import BaseModel, Field

from nashafirma_fastapi.schemas.orders import OrderResponse
from nashafirma_fastapi.schemas.products import ProductResponse


class ItemModel(BaseModel):
    order: int = Field(gt=0)
    product: int = Field(gt=0)
    weight: float = Field(0, ge=0)
    note: str = Field(max_length=250)


class ItemResponse(ItemModel):
    id: int = Field(1, gt=0)
    order: OrderResponse
    product: ProductResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
