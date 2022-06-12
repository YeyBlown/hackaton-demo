# TODO: fill database adapter
# TODO: handle relations post-user on create-like-unlike-delete actions
from fastapi_sqlalchemy import db
from models.models import User as ModelUser
from models.models import Post as ModelPost


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


class PostDBAdapter:
    @staticmethod
    def like_post(user_id: int, post_id: int):
        pass

    @staticmethod
    def unlike_post(user_id: int, post_id: int):
        pass

    @staticmethod
    def create_post():
        pass

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
