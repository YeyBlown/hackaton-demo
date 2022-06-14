""" objects schema by pydantic """
# pylint: disable=no-name-in-module,no-self-argument
# pylint: disable=missing-function-docstring,missing-class-docstring
from pydantic import BaseModel


class Post(BaseModel):
    header: str
    content: str
    author_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    hashed_password: str

    class Config:
        orm_mode = True


class Like(BaseModel):
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
