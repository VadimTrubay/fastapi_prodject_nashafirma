import uuid
from pydantic import Field
from fastapi_users import schemas

class UserModel(schemas.BaseUser[uuid.UUID]):
    pass

class UserRead(schemas.BaseUser[uuid.UUID]):
    user_name: str | None
    first_name: str | None
    last_name: str | None
    phone: str | None


class UserCreate(schemas.BaseUserCreate, UserRead):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserRead):
    pass

