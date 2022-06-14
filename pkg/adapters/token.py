# TODO: refactor
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from adapters.db import DBFacade
from adapters.hash_utils import HashUtils


class TokenAdapter:

    # TODO: move hard variables to contract, please :)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "5d8ff4f4a643f60dd33e0eeafb03fb8741578db760b4b4b08268041cd66d3195"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
