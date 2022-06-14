""" api - analytics related controllers here """
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from adapters.contract import DateTimeEnv
from adapters.db import DBFacade
from services.token import TokenService
from models.models import User as ModelUser

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/likes_by_day")
def likes_by_day(
    date_from: str = Query(default=None, max_length=50),
    date_to: str = Query(default=None, max_length=50),
    current_user: ModelUser = Depends(TokenService.get_current_user),
):
    """returns likes aggregated by dat by given user"""
    time_format = DateTimeEnv.get_date_format()
    date_from_obj = datetime.strptime(date_from, time_format)
    date_to_obj = datetime.strptime(date_to, time_format)
    # TODO: extract common time-related and likes-by-dat functionality
    posts = DBFacade().get_likes_by_user_date(
        date_from_obj, date_to_obj, current_user.id
    )
    likes_by_day_dict = {}
    for post in posts:
        date = post.time_created
        date = date.strftime(time_format)
        likes_by_day_dict[date] = likes_by_day_dict.get(date, 0) + 1
    return likes_by_day_dict


@router.get("/all_likes_by_day")
def all_likes_by_day(date_from: str, date_to: str):
    """returns likes aggregated by dat by all users"""
    time_format = DateTimeEnv.get_date_format()
    date_from_obj = datetime.strptime(date_from, time_format)
    date_to_obj = datetime.strptime(date_to, time_format)

    date_likes_tuples = DBFacade().get_likes_by_user_date(date_from_obj, date_to_obj)
    likes_by_day_dict = dict(date_likes_tuples)
    return likes_by_day_dict


@router.get("/get_all_likes")
def get_all_likes():
    """returns all likes"""
    likes = DBFacade.get_all_likes()
    return likes
