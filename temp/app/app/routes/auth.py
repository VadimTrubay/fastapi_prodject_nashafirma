from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserModel
from app.services.auth import auth_backend, fastapi_users

from app.repository import users as repository_users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# @router.put("/users/update_by_admin", response_model=UserRead)
# async def update_user_by_admin(
#         body: UserUpdate,
#         user: UserRead,
#         db: AsyncSession):
#     user = await repository_users.update_user_by_admin(body, user, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
#     return user
