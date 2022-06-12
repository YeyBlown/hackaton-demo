# TODO user authentification functionality controllers
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from adapters.token import Token, TokenAdapter
from adapters.db import UserDBAdapter
from models.schema import User

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_token_header)], TODO recheck
    responses={404: {"description": "Not found"}},
)


@router.post("/signup")
def signup(username: str, password: str):
    # TODO: check user exists
    # TODO: validate password
    # TODO: add user
    return "user successfully created"


@router.post("/login")
def login(username: str, password: str):
    # TODO: check credentials valid exists
    # TODO: YES: return token
    # TODO: NO: return error
    pass


@router.post("/logout")
def logout(token: str):
    # TODO: check token active
    # TODO: YES: return success, kill token
    # TODO: NO: return error
    pass


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserDBAdapter.get_user_by_username(form_data.username)
    user = TokenAdapter.authenticate_user(user, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TokenAdapter.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenAdapter.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(TokenAdapter.get_current_active_user)):
    return current_user
