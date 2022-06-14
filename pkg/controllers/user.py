# TODO: users related controllers here
from fastapi import APIRouter, Depends

from adapters.db import DBFacade
from adapters.token import TokenAdapter
from models.schema import User as SchemaUser
from models.models import User as ModelUser

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaUser)
def create(user: SchemaUser):
    db_user = DBFacade().create_user(user)
    return db_user


@router.get("/view")
def view():
    users = DBFacade().get_all_users()
    return users


@router.get("/view/my")
async def view_my(
    current_user: ModelUser = Depends(TokenAdapter.get_current_user),
):
    posts = current_user.posts_created
    return posts


@router.get("/activity/{username}")
def user_activity(username: str):
    # TODO: check error properly returned
    user = DBFacade().get_user_by_username(username)
    if not user:
        return {"error": "user does not exist"}
    return {
        "last_login": user.time_last_login,
        "last_activity": user.time_last_activity,
    }
