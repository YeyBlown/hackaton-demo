# TODO user authentification functionality controllers
from fastapi import APIRouter, Depends, HTTPException

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_token_header)], TODO recheck
    responses={404: {"description": "Not found"}},
)


@router.post("/signup")
def signup(login: str, password: str):
    # TODO: check user exists
    # TODO: validate password
    # TODO: add user
    return "user successfully created"


@router.post("/login")
def login(login: str, password: str):
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
