""" user authentication controllers"""
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from services.token import TokenService
from adapters.db import DBFacade
from models.schema import User, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """checks user credential. if all okay updates last_login time and return token"""
    db_adapter = DBFacade()
    user = db_adapter.get_user_by_username(form_data.username)
    user = TokenService.authenticate_user(user, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    db_adapter.update_last_login(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(TokenService.get_current_user),
):
    """returns current user model by credentials"""
    return current_user
