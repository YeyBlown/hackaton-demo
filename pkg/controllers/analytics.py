# TODO: analytics related controllers here
from fastapi import APIRouter, Depends, HTTPException

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    # dependencies=[Depends(get_token_header)], TODO recheck
    responses={404: {"description": "Not found"}},
)


@router.get("/likes_by_day")
def likes_by_day(login: str, date_from: str, date_to: str):
    # TODO: check user exists
    # TODO: YES: return likes by day
    # TODO: NO: return error
    pass


@router.get("/user_activity")
def user_activity(login: str):
    # TODO: check user exists
    # TODO: YES: return (last login, last activity)
    # TODO: NO: return error
    pass
