# TODO: add missing controllers
# TODO: split controllers to controllers modules
# TODO: load parameters
# TODO: create application,
# TODO: do we need startup scripts? Do we place them here?
# TODO: switch db logic to utilizing adapter
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from adapters.token import TokenAdapter
from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser

from models.models import Post as ModelPost
from models.models import User as ModelUser

import os
from dotenv import load_dotenv

from controllers import auth
from adapters.contract import PostgresEnv

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
    db_post = ModelPost(header=post.header, content=post.content, author_id=post.author_id)
    db.session.add(db_post)
    db.session.commit()
    return db_post


@app.get('/post/')
async def post():
    post = db.session.query(ModelPost).all()
    return post


@app.post('/user/', response_model=SchemaUser)
async def user(user: SchemaUser):
    password = user.hashed_password
    hashed_password = TokenAdapter.get_password_hash(password)
    db_user = ModelUser(username=user.username, hashed_password=hashed_password, posts_created=[], post_liked=[])
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get('/user/')
async def user():
    user = db.session.query(ModelUser).all()
    return user


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
