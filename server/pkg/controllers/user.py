""" users related controllers here """
from fastapi import APIRouter, Depends

from adapters.db import DBFacade
from services.token import TokenService
from models.schema import User as SchemaUser
from models.models import User as ModelUser

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=SchemaUser)
def create(user: SchemaUser):
    """creates new user by schema"""
    db_user = DBFacade().create_user(user)
    return db_user


@router.get("/view")
def view(page: int = 0, page_size: int = 10, sort_by: str = 'id', asc_order: bool = True):
    """returns paginated user models"""
    users = DBFacade().get_paginated_users(page, page_size, sort_by, asc_order)
    return users


@router.get("/search")
def view(query: str, search_by: str = 'username', page: int = 0, page_size: int = 10, sort_by: str = 'id', asc_order: bool = True):
    """returns paginated user models"""
    users = DBFacade().search_users(query, search_by, page, page_size, sort_by, asc_order)
    return users


@router.get("/view_all")
def view():
    """returns all user models"""
    users = DBFacade().get_all_users()
    return users


@router.get("/view/my")
async def view_my(
    current_user: ModelUser = Depends(TokenService.get_current_user),
):
    """returns posts created by current user"""
    posts = current_user.posts_created
    return posts


@router.get("/activity/{username}")
def user_activity(username: str):
    """returns activity as last login and last activity times for username"""
    user = DBFacade().get_user_by_username(username)
    if not user:
        return {"error": "user does not exist"}
    return {
        "last_login": user.time_last_login,
        "last_activity": user.time_last_activity,
    }


@router.delete("/user")
def delete_user(
    current_user: ModelUser = Depends(TokenService.get_current_user),
):
    """deletes current user"""
    # TODO: delete all activity associated with the user
    DBFacade().delete_user(current_user)
    return {
        "status": "success"
    }
