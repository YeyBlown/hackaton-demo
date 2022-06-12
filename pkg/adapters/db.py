# TODO: handle relations post-user on create-like-unlike-delete actions
# TODO: ensure thread safe
from fastapi_sqlalchemy import db

from adapters.hash_utils import HashUtils
from models.models import User as ModelUser
from models.models import Post as ModelPost

from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser


class UserDBAdapter:
    @staticmethod
    def get_user_by_username(username: str):
        user = db.session.query(ModelUser).filter_by(username=username).first()
        return user

    @staticmethod
    def get_user_by_id(user_id: int):
        user = db.session.query(ModelUser).filter_by(id=user_id).first()
        return user

    @staticmethod
    def get_all_users():
        users = db.session.query(ModelUser).all()
        return users

    @staticmethod
    def add_post_created():
        pass

    @staticmethod
    def add_post_liked():
        pass

    @staticmethod
    def remove_post_liked():
        pass

    @staticmethod
    def create_user(user: SchemaUser):
        password = user.hashed_password
        hashed_password = HashUtils.get_password_hash(password)
        db_user = ModelUser(username=user.username, hashed_password=hashed_password, posts_created=[], post_liked=[])
        db.session.add(db_user)
        db.session.commit()
        return db_user


class PostDBAdapter:
    @staticmethod
    def like_post(user_id: int, post_id: int):
        pass

    @staticmethod
    def unlike_post(user_id: int, post_id: int):
        pass

    @staticmethod
    def create_post(post: SchemaPost):
        db_post = ModelPost(header=post.header, content=post.content, author_id=post.author_id)
        db.session.add(db_post)
        db.session.commit()
        return db_post

    @staticmethod
    def get_post_by_id(post_id: int):
        post = db.session.query(ModelPost).filter_by(id=post_id).first()
        return post

    @staticmethod
    def get_all_posts():
        posts = db.session.query(ModelPost).all()
        return posts

    @staticmethod
    def get_posts_by_user(user_id: int):
        posts = db.session.query(ModelPost).filter_by(author_id=user_id)
        return posts
