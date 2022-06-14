# TODO: recheck all exceptions handled
# TODO: should i store date of like instead of datetime to group by
import datetime
import threading
from typing import Optional

from fastapi_sqlalchemy import db
from sqlalchemy import and_, func

from adapters.hash_utils import HashUtils
from entities.exceptions import PostAlreadyLikedException, PostIsNotLikedException, ObjectDoesNotExistException
from models.models import User as ModelUser
from models.models import Post as ModelPost
from models.models import Like as ModelLike

from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser


class DBFacade:
    _instance = None
    _lock_instance = threading.Lock()
    _lock = threading.Lock()

    # ensuring our Facade is singleton to apply lock on thread unsafe session operations
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock_instance:
                if not cls._instance:
                    cls._instance = super(DBFacade, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def lock_decorator(lock):
        def decorator(fn):
            def wrapper(*args, **kwargs):
                with lock:
                    result = fn(*args, **kwargs)
                return result
            return wrapper
        return decorator

    def __init__(self):
        self._session = db

    @lock_decorator(_lock)
    def get_user_by_username(self, username: str):
        user = db.session.query(ModelUser).filter_by(username=username).first()
        return user

    @lock_decorator(_lock)
    def get_user_by_id(self, user_id: int):
        user = db.session.query(ModelUser).filter_by(id=user_id).first()
        return user

    @lock_decorator(_lock)
    def get_all_users(self):
        users = db.session.query(ModelUser).all()
        return users

    @lock_decorator(_lock)
    def create_user(self, user: SchemaUser):
        user_db = UserDBAdapter.create_user(user)
        return user_db

    @staticmethod
    def update_last_login(user: ModelUser):
        UserDBAdapter.update_last_login(user)

    @lock_decorator(_lock)
    def create_post(self, user: SchemaUser, post: SchemaPost):
        post_db = PostDBAdapter.create_post(post)
        UserDBAdapter.add_post_created(user, post_db)
        UserDBAdapter.update_last_activity(user)
        return post_db

    @lock_decorator(_lock)
    def get_post_by_id(self, post_id: int):
        post = PostDBAdapter.get_post_by_id(post_id)
        return post

    @lock_decorator(_lock)
    def get_all_posts(self):
        posts = PostDBAdapter.get_all_posts()
        return posts

    @lock_decorator(_lock)
    def get_posts_by_user(self, user_id: int):
        posts_by_user = PostDBAdapter.get_posts_by_user(user_id)
        return posts_by_user

    @lock_decorator(_lock)
    def get_posts_by_user_date(
            self,
            date_from: datetime.datetime,
            date_to: datetime.datetime,
            user_id: Optional[int] = None,
    ):
        posts = PostDBAdapter.get_posts_by_user_date(date_from, date_to, user_id)
        return posts

    @lock_decorator(_lock)
    def like(self, user: ModelUser, post_id: int):
        post = PostDBAdapter.get_post_by_id(post_id)
        if not post:  # TODO: recheck works properly
            raise ObjectDoesNotExistException()
        like_db = LikeDBAdapter.create(user, post)
        UserDBAdapter._add_like(user, like_db)
        PostDBAdapter._add_like(post, like_db)
        UserDBAdapter.update_last_activity(user)
        return like_db

    @lock_decorator(_lock)
    def unlike(self, user: ModelUser, post_id: int):
        post = PostDBAdapter.get_post_by_id(post_id)
        like = LikeDBAdapter.get_like(user.id, post.id)
        if not like:
            raise PostIsNotLikedException()
        UserDBAdapter._remove_like(user, like)
        PostDBAdapter._remove_like(post, like)
        db.session.query(ModelLike).filter(and_(ModelLike.id == like.id)).delete()
        UserDBAdapter.update_last_activity(user)


class UserDBAdapter:

    @staticmethod
    def add_post_created(user: ModelUser, post: ModelPost):
        user.posts_created.append(post)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def create_user(user: SchemaUser):
        password = user.hashed_password
        hashed_password = HashUtils.get_password_hash(password)
        user_db = ModelUser(
            username=user.username,
            hashed_password=hashed_password,
            posts_created=[],
            likes=[],
        )
        db.session.add(user_db)
        db.session.commit()
        return user_db

    @staticmethod
    def update_last_login(user: ModelUser):
        time_now = datetime.datetime.now()
        user.time_last_login = time_now
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update_last_activity(user: ModelUser):
        time_now = datetime.datetime.now()
        user.time_last_activity = time_now
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def _add_like(user: ModelUser, like: ModelLike):
        user.likes.append(like)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def _remove_like(user: ModelUser, like: ModelLike):
        user.likes.remove(like)
        db.session.add(user)
        db.session.commit()


class PostDBAdapter:
    @staticmethod
    def create_post(post: SchemaPost):
        post_db = ModelPost(
            header=post.header, content=post.content, author_id=post.author_id
        )
        db.session.add(post_db)
        db.session.commit()
        return post_db

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

    @staticmethod
    def get_posts_by_user_date(
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        user_id: Optional[int] = None,
    ):
        condition = and_(
                    func.date(ModelPost.time_created) >= date_from,
                    func.date(ModelPost.time_created) <= date_to,
                ) if user_id is None else and_(
                    func.date(ModelPost.time_created) >= date_from,
                    func.date(ModelPost.time_created) <= date_to,
                    ModelPost.author_id == user_id,
                )
        query = db.session.query(ModelPost).filter(condition)
        return [e for e in query]

    @staticmethod
    def _add_like(post: ModelPost, like: ModelLike):
        post.likes.append(like)
        db.session.add(like)
        db.session.commit()

    @staticmethod
    def _remove_like(post: ModelPost, like: ModelLike):
        post.likes.remove(like)
        db.session.add(post)
        db.session.commit()


class LikeDBAdapter:
    @staticmethod
    def create(user: ModelUser, post: ModelPost):
        if LikeDBAdapter.is_like_exists(user.id, post.id):
            raise PostAlreadyLikedException()
        like_db = ModelLike(
            user_id=user.id,
            post_id=post.id,
            user=user,
            post=post
        )
        db.session.add(like_db)
        db.session.commit()
        return like_db

    @staticmethod
    def is_like_exists(user_id: id, post_id: id):
        return True if LikeDBAdapter.get_like(user_id, post_id) else False

    @staticmethod
    def get_like(user_id: id, post_id: id):
        like = db.session.query(ModelLike).filter(
            and_(
                ModelLike.user_id == user_id,
                ModelLike.post_id == post_id
            )
        ).first()
        return like