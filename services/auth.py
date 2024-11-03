"""Модуль який відповідає за всі операції поа'язані з авторизацією користувача
Функціонал:
1. Хешування паролю
2. Звірення хешованого паролю з введенним
3. Створення access, email verification і refresh токенів
4. Декодування refresh токену
5. Отримання поточного юзера
6. Отримання email з токена підтвердження
"""

import pickle
import uuid
from datetime import datetime, timedelta
from typing import Optional

import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from nashafirma_fastapi.conf import detail
from nashafirma_fastapi.conf.config import settings
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.repository import users as repository_users
from passlib.context import CryptContext
from sqlalchemy.orm import Session


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail.NOT_VALIDATE,
        headers={"WWW-Authenticate": "Bearer"},
    )
    cache = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    async def blocklist(self, token):
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        if payload.get("scope") == "access_token":
            email = payload.get("sub")
            if email is None:
                raise self.credentials_exception
            jti = payload.get("jti")
            if jti is None:
                raise self.credentials_exception
            await self.cache.set(jti, "true")

    def is_blocklisted(self, jti):
        return self.cache.exists(jti)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            "iat": datetime.utcnow(),
            "exp": expire,
            "scope": "access_token",
            "jti": str(uuid.uuid4()),
        }
        to_encode.update(payload)
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    def required_auth_with_email(self, token: str = Depends(oauth2_scheme)):
        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise self.credentials_exception
                jti = payload.get("jti")
                if jti is None:
                    raise self.credentials_exception
                if self.is_blocklisted(jti):
                    raise self.credentials_exception
                return email
            else:
                raise self.credentials_exception
        except JWTError:
            raise self.credentials_exception

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        email = self.required_auth_with_email(token)

        user = self.cache.get(f"user:{email}")
        if user is None:
            print("User from database")
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise self.credentials_exception
            self.cache.set(f"user:{email}", pickle.dumps(user))  # noqa
            self.cache.expire(f"user:{email}", 120)  # noqa need change this time of 900
        else:
            print("User from cash")
            user = pickle.loads(user)  # noqa

        if user is None:
            raise self.credentials_exception
        return user

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.INVALID_TOKEN
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.NOT_VALIDATE
            )

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"}
        )
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload["scope"] == "email_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=detail.INVALID_TOKEN
            )
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail.INVALID_TOKEN_EMAIL,
            )


auth_service = Auth()
