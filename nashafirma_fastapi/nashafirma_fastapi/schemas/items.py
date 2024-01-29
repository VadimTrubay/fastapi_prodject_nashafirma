from datetime import date

from pydantic import BaseModel, Field


class ItemModel(BaseModel):
    order: int = Field(gt=0)
    product: int = Field(gt=0)
    weight: float = Field(ge=0)
    note: str = Field(max_length=250)


class ItemResponse(ItemModel):
    id: int
    order: int
    product: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class ItemCreate(ItemModel):
    pass
