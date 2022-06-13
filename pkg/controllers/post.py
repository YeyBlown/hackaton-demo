# posts related controllers here
from fastapi import APIRouter, Depends

from adapters.db import PostDBAdapter, UserDBAdapter
from models.schema import Post as SchemaPost
from models.schema import User
from adapters.token import TokenAdapter

router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaPost)
async def create(post: SchemaPost, current_user: User = Depends(TokenAdapter.get_current_active_user)):
    db_post = PostDBAdapter.create_post(post)
    _ = UserDBAdapter.add_post_created(current_user, db_post)
    UserDBAdapter.update_last_activity(current_user)
    return db_post


@router.post("/like")
async def like(post: SchemaPost, current_user: User = Depends(TokenAdapter.get_current_active_user)):
    db_post = PostDBAdapter.like_post(current_user, post)
    _ = UserDBAdapter.add_post_liked(current_user, db_post)
    UserDBAdapter.update_last_activity(current_user)
    return db_post


@router.post("/unlike")
async def unlike(post: SchemaPost, current_user: User = Depends(TokenAdapter.get_current_active_user)):
    #  TODO: check post liked by user
    #  TODO: YES: unlike, return success
    #  TODO: NO: return "not liked"
    db_post = PostDBAdapter.unlike_post(current_user, post)
    _ = UserDBAdapter.remove_post_liked(current_user, db_post)
    UserDBAdapter.update_last_activity(current_user)
    return db_post


@router.get("/view")
def view():
    posts = PostDBAdapter.get_all_posts()
    return posts