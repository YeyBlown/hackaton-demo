""" posts related controllers here"""
from fastapi import APIRouter, Depends

from adapters.db import DBFacade
from services.token import TokenService
from entities.exceptions import (
    PostAlreadyLikedException,
    PostIsNotLikedException,
    ObjectDoesNotExistException,
)
from models.schema import Post as SchemaPost
from models.models import User as ModelUser

router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaPost)
async def create(
    post: SchemaPost, current_user: ModelUser = Depends(TokenService.get_current_user)
):
    """creates new post by schema"""
    db_post = DBFacade().create_post(current_user, post, current_user.id)
    return db_post


@router.post("/like")
async def like(
    post_id: int, current_user: ModelUser = Depends(TokenService.get_current_user)
):
    """likes post as current_user by post_id"""
    try:
        like_db = DBFacade().like(current_user, post_id)
    except PostAlreadyLikedException:
        return {"error": "already liked"}
    except ObjectDoesNotExistException:
        return {"error": "post does not exist"}
    return like_db


@router.post("/unlike")
async def unlike(
    post_id: int, current_user: ModelUser = Depends(TokenService.get_current_user)
):
    """removes like as current_user by post_id"""
    try:
        DBFacade().unlike(current_user, post_id)
    except PostIsNotLikedException:
        return {"error": "not yet liked liked"}
    except ObjectDoesNotExistException:
        return {"error": "post does not exist"}


@router.get("/view")
def view():
    """returns all posts to see"""
    posts = DBFacade().get_all_posts()
    return posts
