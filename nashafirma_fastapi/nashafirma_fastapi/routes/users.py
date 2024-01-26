from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.database.models import User
from nashafirma_fastapi.schemas.users import UserResponse, UserModel, UserUpdate
from nashafirma_fastapi.repository import users as repository_users
from services.auth import auth_service
# from services.cloud_image import CloudImage

router = APIRouter(prefix="/users", tags=["users"])

security = HTTPBearer()


@router.get("/me",
            response_model=UserResponse
            )
async def get_user_me(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_users.get_me(current_user, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result


@router.patch('/me/',
              response_model=UserResponse
              )
async def update_user(
        body: UserUpdate,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_users.update(current_user, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result


# @router.patch('/avatar',
#               response_model=UserResponse
#               )
# async def update_avatar_user(
#         file: UploadFile = File(),
#         current_user: User = Depends(auth_service.get_current_user),
#         db: Session = Depends(get_db)
# ):
#     public_id = CloudImage.generate_name_avatar(current_user.email)
#     r = CloudImage.upload(file.file, public_id)
#     src_url = CloudImage.get_url_for_avatar(public_id, r)
#     user = await repository_users.update_avatar(current_user.email, src_url, db)
#     return user


@router.delete("/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def remove_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    result = await repository_users.remove(user_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result
