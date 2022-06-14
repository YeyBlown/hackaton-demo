from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from adapters.contract import EncryptionEnv
from adapters.db import DBFacade
from adapters.hash_utils import HashUtils


class TokenAdapter:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=EncryptionEnv.get_token_url())
    SECRET_KEY = EncryptionEnv.get_token_secret_key()
    ALGORITHM = EncryptionEnv.get_token_algorithm()
    ACCESS_TOKEN_EXPIRE_MINUTES = int(EncryptionEnv.get_access_token_expire_minutes())

    @staticmethod
    def authenticate_user(user, password: str):
        if not user:
            return False
        if not HashUtils.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, TokenAdapter.SECRET_KEY, algorithm=TokenAdapter.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, TokenAdapter.SECRET_KEY, algorithms=[TokenAdapter.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = DBFacade().get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
