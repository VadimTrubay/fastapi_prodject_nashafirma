from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from app.database.app_db import get_db
from app.database.models import User
from app.schemas.users import UserCreate, UserUpdate, UserModel, UserRead


# async def update_user_by_admin(body: UserUpdate, user: UserRead, db: AsyncSession = Depends(get_db)):
#     user = select(User).filter_by(user=user)
#     result = await db.execute(user)
#     is_admin = result.scalar_one_or_none()
#     if is_admin:
#         is_admin.is_superuser = body.is_superuser
#         await db.commit()
#         await db.refresh(is_admin)
#     return is_admin


# async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
#     stmt = select(User).filter_by(email=email)
#     user = await db.execute(stmt)
#     user = user.scalar_one_or_none()
#     return user
#
#
# async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
#     avatar = None
#     try:
#         g = Gravatar(body.email)
#         avatar = g.get_image()
#     except Exception as err:
#         print(err)
#
#     new_user = User(**body.model_dump(), avatar=avatar)
#     get_len_db = await db.execute(select(User))
#     print(len(get_len_db.scalars().all()))
#     if len(get_len_db.scalars().all()) == 0:  # First user always admin
#         new_user.is_superuser = True  # active
#         print(new_user.is_superuser)
#         db.add(new_user)
#         await db.commit()
#         await db.refresh(new_user)
#     return new_user
#
#
# async def update_token(user: User, token: str | None, db: AsyncSession):
#     user.refresh_token = token
#     await db.commit()