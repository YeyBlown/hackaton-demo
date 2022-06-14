""" module for service to operate with date and time """
import datetime
from fastapi import Query

from adapters.contract import DateTimeEnv


class DateTimeService:
    """ service for operating with date and time """

    @staticmethod
    def datetime_from_str(datetime_str: str = Query(default=None, max_length=50)):
        datetime_obj = datetime.datetime.strptime(datetime_str, DateTimeEnv.get_date_format())
        return datetime_obj

    @staticmethod
    def datetime_to_str(datetime_obj: datetime.datetime):
        datetime_str = datetime_obj.strftime(DateTimeEnv.get_date_format())
        return datetime_str

    @staticmethod
    def get_today_datetime():
        date_today = datetime.date.today()
        datetime_today = datetime.datetime(
            year=date_today.year, month=date_today.month, day=date_today.day
        )
        return datetime_today

