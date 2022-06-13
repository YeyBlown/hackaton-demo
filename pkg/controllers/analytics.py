# TODO: analytics related controllers here
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from adapters.db import PostDBAdapter
from adapters.token import TokenAdapter
from models.schema import User

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    # dependencies=[Depends(get_token_header)], TODO: recheck
    responses={404: {"description": "Not found"}},
)


@router.get("/likes_by_day")
def likes_by_day(date_from: str = Query(default=None, max_length=50), date_to: str= Query(default=None, max_length=50), current_user: User = Depends(TokenAdapter.get_current_active_user)):
    time_format = '%Y-%m-%d' # TODO: move to env
    date_from_obj = datetime.strptime(date_from, time_format)
    date_to_obj = datetime.strptime(date_to, time_format)

    # TODO: do to likes by day, not posts
    posts = PostDBAdapter.get_posts_by_user_date(date_from_obj, date_to_obj, current_user.id)
    likes_by_day = {}
    for post in posts:
        date = post.time_created
        date = date.strftime(time_format)
        likes_by_day[date] = likes_by_day.get(date, 0) + 1
    return likes_by_day


@router.get("/likes_by_day_general")
def likes_by_day(date_from: str, date_to: str):
    date_from_obj = datetime.strptime(date_from, '%y/%m/%d')
    date_to_obj = datetime.strptime(date_to, '%y/%m/%d')
    # TODO: calculate by day

    # TODO: check user exists
    # TODO: YES: return likes by day
    # TODO: NO: return error
    pass
