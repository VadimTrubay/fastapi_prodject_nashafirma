from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from nashafirma_fastapi.conf import detail
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.repository import users as repository_users
from nashafirma_fastapi.schemas.users import (
    UserModel,
    UserResponse,
    TokenModel,
    RequestEmail,
)
from services.auth import auth_service
from services.email import send_email
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=detail.ACCOUNT_AlREADY_EXISTS
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, str(request.base_url)
    )
    # return {"user": new_user.username, "detail": detail.SUCCESS_CREATE_USER}
    return new_user


@router.post(
    "/login",
    response_model=TokenModel,
)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.INVALID_EMAIL
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.EMAIL_NOT_CONFIRMED
        )
    # Check is_active
    # if not user.is_active:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail.USER_NOT_ACTIVE)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.INVALID_PASSWORD
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    token = credentials.credentials
    await auth_service.blocklist(token)
    return {"message": detail.USER_IS_LOGOUT}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail.INVALID_REFRESH_TOKEN,
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail.VERIFICATION_ERROR
        )
    if user.confirmed:
        return {"message": detail.ALREADY_CONFIRMED}
    await repository_users.confirmed_email(email, db)
    return {"message": detail.EMAIL_CONFIRMED}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        if user.confirmed:
            return {"message": detail.ALREADY_CONFIRMED}
        background_tasks.add_task(
            send_email, user.email, user.username, str(request.base_url)
        )
    return {"message": detail.CHECK_CONFIRMATION}
