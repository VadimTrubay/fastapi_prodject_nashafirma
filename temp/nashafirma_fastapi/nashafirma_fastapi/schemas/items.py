from datetime import datetime

from pydantic import BaseModel, Field


class InItem(BaseModel):
    order: int = Field(gt=0)
    product: int = Field(gt=0)
    weight: float = Field(0, ge=0)
    note: str = Field(max_length=250)


class OutItem(InItem):
    id: int = Field(1, gt=0)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
