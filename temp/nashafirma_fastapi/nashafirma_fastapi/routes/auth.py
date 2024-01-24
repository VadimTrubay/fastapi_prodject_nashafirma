from fastapi import APIRouter
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()




