# TODO
from typing import List

from pandas import Timestamp
from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    id: UUID
    login: str
    password: str
    last_login: Timestamp
    last_activity: Timestamp
    posts_created: List[str]
    posts_liked: List[str]
