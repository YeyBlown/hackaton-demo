# TODO: get controllers
# TODO: load parameters
# TODO: create application,
# TODO: do we need startup scripts? Do we place them here?
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser

from models.models import Post as ModelPost
from models.models import User as ModelUser

import os
from dotenv import load_dotenv

load_dotenv('local.env')

app = FastAPI()

# to avoid csrftokenError
# db_url = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


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
    db_user = ModelUser(login=user.login, password=user.password, posts_created=[], post_liked=[])
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
