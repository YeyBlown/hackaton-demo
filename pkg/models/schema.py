# build a schema using pydantic
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
