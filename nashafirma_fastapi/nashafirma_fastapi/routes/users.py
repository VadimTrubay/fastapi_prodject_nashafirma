import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer
from nashafirma_fastapi.conf.config import settings
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.database.models import User
from nashafirma_fastapi.repository import users as repository_users
from nashafirma_fastapi.schemas.users import UserResponse, UserUpdate
from services.auth import auth_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

security = HTTPBearer()


@router.get("/me", response_model=UserResponse)
async def get_user_me(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    result = await repository_users.get_me(current_user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return result


@router.patch("/me/", response_model=UserResponse)
async def update_user(
    body: UserUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    result = await repository_users.update(current_user, body, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return result


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f"nashafirma/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(
        f"nashafirma/{current_user.username}"
    ).build_url(width=150, height=150, crop="fill", version=r.get("version"))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


# @router.patch(
#     "/avatar",
#     response_model=UserResponse,
# )
# async def get_current_user(
#     file: UploadFile = File(),
#     user: User = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     public_id = f"nashafirma/{user.email}"
#     res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
#     print(res)
#     res_url = cloudinary.CloudinaryImage(public_id).build_url(
#         width=150, height=150, crop="fill", version=res.get("version")
#     )
#     user = await repository_users.update_avatar(user.email, res_url, db)
#     auth_service.cache.set(user.email, pickle.dumps(user))
#     auth_service.cache.expire(user.email, 300)
#     return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    result = await repository_users.remove(user_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return result
