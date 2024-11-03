from pydantic import BaseModel, Field

from nashafirma_fastapi.schemas.orders import OrderFromItem
from nashafirma_fastapi.schemas.products import ProductFromItem


class ItemModel(BaseModel):
    order: int = Field(gt=0)
    product: int = Field(gt=0)
    weight: float = Field(ge=0)
    note: str = Field(max_length=250)


class ItemResponse(BaseModel):
    id: int
    order: OrderFromItem
    order_id: int
    product: ProductFromItem
    product_id: int
    # created_at: date
    # updated_at: date

    class Config:
        from_attributes = True


class ItemFromOrder(BaseModel):
    id: int
    order: OrderFromItem
    order_id: int
    product: str
    product_id: int

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    order_id: int
    product_id: int
    weight: float
    note: str
