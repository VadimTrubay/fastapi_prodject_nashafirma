from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.users import UserRead

class InOrder(BaseModel):
    done: bool = Field(False)
    user: int = Field(1, gt=0)


class OutOrder(InOrder):
    id: int = Field(1, gt=0)
    created_at: datetime
    updated_at: datetime
    user: UserRead

    class Config:
        from_attributes = True

