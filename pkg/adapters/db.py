# TODO: fill database adapter
from fastapi_sqlalchemy import db
from models.models import User as ModelUser


class UserDBAdapter:
    @staticmethod
    def get_user_by_username(username: str):
        user = db.session.query(ModelUser).filter_by(username=username).first()
        return user

    @staticmethod
    def get_user_by_id():
        pass

    @staticmethod
    def get_all_users():
        pass

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
    def like_post():
        pass

    @staticmethod
    def unlike_post():
        pass

    @staticmethod
    def create_post():
        pass

    @staticmethod
    def get_post_by_id():
        pass

    @staticmethod
    def get_all_posts():
        pass

    @staticmethod
    def get_post_by_user():
        pass
