# TODO: users related controllers here
from fastapi import APIRouter

from adapters.db import UserDBAdapter
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