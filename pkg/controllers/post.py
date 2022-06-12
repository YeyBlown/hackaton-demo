# TODO: posts related controllers here
from fastapi import APIRouter

from adapters.db import PostDBAdapter
from models.schema import Post as SchemaPost

router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaPost)
def create(token: str, post: SchemaPost):
    # TODO
    db_post = PostDBAdapter.create_post(post)
    return db_post


@router.post("/like")
def like(token: str, post_id: str):
    pass


@router.post("/unlike")
def unlike(token: str, post_id: str):
    # TODO: check post exists
    #  TODO: check post liked by user
    #  TODO: YES: unlike, return success
    #  TODO: NO: return "not liked"
    pass


@router.get("/view")
def view():
    posts = PostDBAdapter.get_all_posts()
    return posts