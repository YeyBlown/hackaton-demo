# TODO: add missing controllers
# TODO: split controllers to controllers modules
# TODO: load parameters
# TODO: do we need startup scripts? Do we place them here?
# TODO: switch db logic to utilizing adapter
from dotenv import load_dotenv
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from adapters.contract import PostgresEnv
from adapters.db import UserDBAdapter
from adapters.db import PostDBAdapter
from adapters.token import TokenAdapter

from controllers import auth

from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser

from models.models import Post as ModelPost
from models.models import User as ModelUser


load_dotenv('local.env')

app = FastAPI()

app.include_router(auth.router)

# to avoid csrftokenError
# db_url = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'
app.add_middleware(DBSessionMiddleware, db_url=PostgresEnv.get_url())


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/post/', response_model=SchemaPost)
async def post(post: SchemaPost):
    db_post = PostDBAdapter.create_post(post)
    return db_post


@app.get('/post/')
async def post():
    posts = PostDBAdapter.get_all_posts()
    return posts


@app.post('/user/', response_model=SchemaUser)
async def user(user: SchemaUser):
    db_user = UserDBAdapter.create_user(user)
    return db_user


@app.get('/user/')
async def user():
    users = UserDBAdapter.get_all_users()
    return users


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
