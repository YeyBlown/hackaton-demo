# TODO
from typing import List

from pydantic import BaseModel
from uuid import UUID


class Post(BaseModel):
    id: UUID
    header: str
    content: str
    author: str
    users_liked: List[str]
