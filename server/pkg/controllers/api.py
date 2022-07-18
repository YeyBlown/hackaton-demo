""" api - analytics related controllers here """
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from adapters.contract import DateTimeEnv
from adapters.db import DBFacade
from services.datetimeservice import DateTimeService
from services.token import TokenService
from models.models import User as ModelUser

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/likes_by_day")
def likes_by_day(
    date_from_obj: datetime = Depends(DateTimeService.datetime_from_str),
    date_to_obj: datetime = Depends(DateTimeService.datetime_from_str),
    current_user: ModelUser = Depends(TokenService.get_current_user),
):
    """returns likes aggregated by dat by given user"""
    date_likes_tuples = DBFacade().get_likes_by_user_date(
        date_from_obj, date_to_obj, current_user.id
    )
    return dict(date_likes_tuples)


@router.get("/all_likes_by_day")
def all_likes_by_day(date_from: str, date_to: str):
    """returns likes aggregated by dat by all users"""
    time_format = DateTimeEnv.get_date_format()
    date_from_obj = datetime.strptime(date_from, time_format)
    date_to_obj = datetime.strptime(date_to, time_format)

    date_likes_tuples = DBFacade().get_likes_by_user_date(date_from_obj, date_to_obj)
    return dict(date_likes_tuples)


@router.get("/get_all_likes")
def get_all_likes():
    """returns all likes"""
    likes = DBFacade.get_all_likes()
    return likes
