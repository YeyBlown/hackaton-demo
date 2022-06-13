# TODO: users related controllers here
from fastapi import APIRouter, Depends

from adapters.db import UserDBAdapter
from adapters.token import TokenAdapter
from models.schema import User as SchemaUser

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaUser)
def create(user: SchemaUser):
    # TODO
    db_user = UserDBAdapter.create_user(user)
    return db_user


@router.get("/view")
def view():
    users = UserDBAdapter.get_all_users()
    return users


@router.get("/view/my")
async def view_my(
    current_user: SchemaUser = Depends(TokenAdapter.get_current_active_user),
):
    posts = current_user.posts_created
    return posts


@router.get("/activity/{username}")
def user_activity(username: str):
    # TODO: check user exists
    # TODO: NO: return error
    user = UserDBAdapter.get_user_by_username(username)
    return {
        "last_login": user.time_last_login,
        "last_activity": user.time_last_activity,
    }
