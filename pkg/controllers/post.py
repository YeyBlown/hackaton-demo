# posts related controllers here
from fastapi import APIRouter, Depends

from adapters.db import PostDBAdapter, UserDBAdapter, LikeDBAdapter
from entities.exceptions import PostAlreadyLikedException, PostIsNotLikedException
from models.schema import Post as SchemaPost
from models.schema import User
from adapters.token import TokenAdapter

router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaPost)
async def create(
    post: SchemaPost, current_user: User = Depends(TokenAdapter.get_current_active_user)
):
    db_post = PostDBAdapter.create_post(post)
    _ = UserDBAdapter.add_post_created(current_user, db_post)
    UserDBAdapter.update_last_activity(current_user)
    return db_post


@router.post("/like")
async def like(
    post_id: int, current_user: User = Depends(TokenAdapter.get_current_active_user)
):
    post = PostDBAdapter.get_post_by_id(post_id)
    try:
        like_db = LikeDBAdapter.create(current_user, post)
    except PostAlreadyLikedException as _:
        return {"error": 'already liked'}
    UserDBAdapter.update_last_activity(current_user)
    return like_db


@router.post("/unlike")
async def unlike(
    post_id: int, current_user: User = Depends(TokenAdapter.get_current_active_user)
):
    post = PostDBAdapter.get_post_by_id(post_id)
    try:
        like_db = LikeDBAdapter.remove(current_user, post)
    except PostIsNotLikedException as _:
        return 'not yet liked to unlike'
    UserDBAdapter.update_last_activity(current_user)
    return like_db


@router.get("/view")
def view():
    posts = PostDBAdapter.get_all_posts()
    return posts
