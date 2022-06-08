# TODO: posts related controllers here
from fastapi import APIRouter, Depends, HTTPException

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/post",
    tags=["post"],
    # dependencies=[Depends(get_token_header)], TODO recheck
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
def create(token: str, header: str, content: str):
    pass


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
    # TODO: return posts
    # TODO: figure out better way than returning all posts
    pass