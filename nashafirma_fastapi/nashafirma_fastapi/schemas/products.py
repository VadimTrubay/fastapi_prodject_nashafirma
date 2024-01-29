from pydantic import BaseModel, Field
from pydantic.types import date


class ProductModel(BaseModel):
    product: str = Field(max_length=50)
    price: float = Field(0, ge=0, le=2500)


class ProductResponse(ProductModel):
    id: int = Field(1, gt=0)
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
