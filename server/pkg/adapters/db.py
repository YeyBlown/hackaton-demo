""" cold storage related functionality module """
import datetime
import threading
from typing import Optional

from fastapi_sqlalchemy import db
from sqlalchemy import and_, func, desc, asc

from adapters.hash_utils import HashUtils
from entities.exceptions import (
    PostAlreadyLikedException,
    PostIsNotLikedException,
    ObjectDoesNotExistException,
    UsernameBusyException,
)
from models.models import User as ModelUser
from models.models import Post as ModelPost
from models.models import Like as ModelLike

from models.schema import Post as SchemaPost
from models.schema import User as SchemaUser
from services.datetimeservice import DateTimeService


class DBFacade:
    """main and only facade for interacting with database"""

    _instance = None
    _lock_instance = threading.Lock()
    _lock = threading.Lock()

    # pylint: disable=unused-argument
    def __new__(cls, *args, **kwargs):
        """ensuring our Facade is singleton to apply lock on thread unsafe session operations"""
        if not cls._instance:
            with cls._lock_instance:
                if not cls._instance:
                    cls._instance = super(DBFacade, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def lock_decorator(lock):
        """generic decorator to lock thread unsafe db.session"""

        def decorator(function):
            def wrapper(*args, **kwargs):
                with lock:
                    result = function(*args, **kwargs)
                return result

            return wrapper

        return decorator

    @lock_decorator(_lock)
    def get_user_by_username(self, username: str):
        """returns user model by username"""
        user = db.session.query(ModelUser).filter_by(username=username).first()
        return user

    @lock_decorator(_lock)
    def get_user_by_id(self, user_id: int):
        """returns user model by id"""
        user = db.session.query(ModelUser).filter_by(id=user_id).first()
        return user

    @lock_decorator(_lock)
    def get_all_users(self):
        """returns all user models"""
        users = db.session.query(ModelUser).all()
        return users

    @lock_decorator(_lock)
    def get_paginated_users(self, page, page_size, sort_by, asc_order):
        """returns all user models"""
        users = _UserDBAdapter.query_paginated_users(page, page_size, sort_by, asc_order)
        return users

    @lock_decorator(_lock)
    def search_users(self, query, search_by, page, page_size, sort_by, asc_order):
        """returns all user models"""
        users = _UserDBAdapter.search_paginated_users(query, search_by, page, page_size, sort_by, asc_order)
        return users

    @lock_decorator(_lock)
    def create_user(self, user: SchemaUser):
        """creates new user model by schema and stores it"""
        user_db = _UserDBAdapter.create_user(user)
        return user_db

    @lock_decorator(_lock)
    def delete_user(self, user: ModelUser):
        """deletes given user"""
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def update_last_login(user: ModelUser):
        """updates user's last_login field by time now"""
        _UserDBAdapter.update_last_login(user)

    @lock_decorator(_lock)
    def create_post(self, user: SchemaUser, post: SchemaPost, author_id):
        """creates new post model by schema and stores it"""
        post_db = _PostDBAdapter.create_post(post, author_id)
        _UserDBAdapter.add_post_created(user, post_db)
        _UserDBAdapter.update_last_activity(user)
        return post_db

    @lock_decorator(_lock)
    def get_all_posts(self):
        """returns all user models"""
        posts = _PostDBAdapter.get_all_posts()
        return posts

    @lock_decorator(_lock)
    def get_posts_by_user(self, user_id: int):
        """returns all post models with matching authod_id"""
        posts_by_user = _PostDBAdapter.get_posts_by_user(user_id)
        return posts_by_user

    @lock_decorator(_lock)
    def get_likes_by_user_date(
        self,
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        user_id: Optional[int] = None,
    ):
        """returns likes made by user between given dates"""
        likes = _LikeDBAdapter.get_likes_by_user_date(date_from, date_to, user_id)
        return likes

    @lock_decorator(_lock)
    def like(self, user: ModelUser, post_id: int):
        """likes post for user"""
        post = _PostDBAdapter.get_post_by_id(post_id)
        if not post:
            raise ObjectDoesNotExistException()
        like_db = _LikeDBAdapter.create(user, post)
        _UserDBAdapter.add_like(user, like_db)
        _PostDBAdapter.add_like(post, like_db)
        _UserDBAdapter.update_last_activity(user)
        return like_db

    @lock_decorator(_lock)
    def unlike(self, user: ModelUser, post_id: int):
        """removes like made by user from post by post_id"""
        post = _PostDBAdapter.get_post_by_id(post_id)
        like = _LikeDBAdapter.get_like(user.id, post.id)
        if not like:
            raise PostIsNotLikedException()
        _UserDBAdapter.remove_like(user, like)
        _PostDBAdapter.remove_like(post, like)
        db.session.query(ModelLike).filter(and_(ModelLike.id == like.id)).delete()
        _UserDBAdapter.update_last_activity(user)

    @staticmethod
    def get_all_likes():
        """returns all like models"""
        return db.session.query(ModelLike).all()


class _UserDBAdapter:
    @staticmethod
    def add_post_created(user: ModelUser, post: ModelPost):
        """add given post to created by given user"""
        user.posts_created.append(post)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def create_user(user: SchemaUser):
        """creates and stores new user model by post schema"""
        identical_user = (
            db.session.query(ModelUser).filter_by(username=user.username).first()
        )
        if identical_user:
            raise UsernameBusyException()
        password = user.hashed_password
        hashed_password = HashUtils.get_password_hash(password)
        user_db = ModelUser(
            username=user.username,
            hashed_password=hashed_password,
            name=user.name,
            surname=user.surname,
            description=user.description,
            age=user.age,
            posts_created=[],
            likes=[],
        )
        db.session.add(user_db)
        db.session.commit()
        return user_db

    @staticmethod
    def update_last_login(user: ModelUser):
        """updates last user login by datetime.now()"""
        time_now = datetime.datetime.now()
        user.time_last_login = time_now
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update_last_activity(user: ModelUser):
        """updates last user activity by datetime.now()"""
        time_now = datetime.datetime.now()
        user.time_last_activity = time_now
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_like(user: ModelUser, like: ModelLike):
        """adds like to given user model"""
        user.likes.append(like)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def remove_like(user: ModelUser, like: ModelLike):
        """removes like from given user model"""
        user.likes.remove(like)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def query_paginated_users(page, page_size, sort_by, asc_order):
        users = db.session.query(ModelUser).order_by(asc(sort_by) if asc_order else desc(sort_by)).\
            limit(page_size).offset(page * page_size).all()
        return users

    @staticmethod
    def search_paginated_users(query, search_by, page, page_size, sort_by, asc_order):
        users = db.session.query(ModelUser).filter(ModelUser.username.regexp_match(query)).\
            order_by(asc(sort_by) if asc_order else desc(sort_by)).\
            limit(page_size).offset(page * page_size).all()
        return users


class _PostDBAdapter:
    @staticmethod
    def create_post(post: SchemaPost, author_id):
        """creates and stores new post model by post schema"""
        post_db = ModelPost(
            header=post.header, content=post.content, author_id=author_id
        )
        db.session.add(post_db)
        db.session.commit()
        return post_db

    @staticmethod
    def get_post_by_id(post_id: int):
        """returns post by post_id"""
        post = db.session.query(ModelPost).filter_by(id=post_id).first()
        if not post:
            raise ObjectDoesNotExistException()
        return post

    @staticmethod
    def get_all_posts():
        """returns all posts"""
        posts = db.session.query(ModelPost).all()
        return posts

    @staticmethod
    def get_posts_by_user(user_id: int):
        """returns all posts created by user"""
        posts = db.session.query(ModelPost).filter_by(author_id=user_id)
        return posts

    @staticmethod
    def add_like(post: ModelPost, like: ModelLike):
        """adds given like to post"""
        post.likes.append(like)
        db.session.add(like)
        db.session.commit()

    @staticmethod
    def remove_like(post: ModelPost, like: ModelLike):
        """remove given like from post"""
        post.likes.remove(like)
        db.session.add(post)
        db.session.commit()


class _LikeDBAdapter:
    @staticmethod
    def create(user: ModelUser, post: ModelPost):
        """creates new like from user to post"""
        if _LikeDBAdapter.is_like_exists(user.id, post.id):
            raise PostAlreadyLikedException()
        time_created = DateTimeService.get_today_datetime()
        like_db = ModelLike(
            user_id=user.id,
            post_id=post.id,
            user=user,
            post=post,
            time_created=time_created,
        )
        db.session.add(like_db)
        db.session.commit()
        return like_db

    @staticmethod
    def is_like_exists(user_id: id, post_id: id):
        """return True if like exists else False"""
        try:
            _LikeDBAdapter.get_like(user_id, post_id)
            return True
        except ObjectDoesNotExistException:
            return False

    @staticmethod
    def get_like(user_id: id, post_id: id):
        """returns like by user_id and post_id"""
        like = (
            db.session.query(ModelLike)
            .filter(and_(ModelLike.user_id == user_id, ModelLike.post_id == post_id))
            .first()
        )
        if not like:
            raise ObjectDoesNotExistException()
        return like

    @staticmethod
    def get_likes_by_user_date(
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        user_id: Optional[int] = None,
    ):
        """returns likes grouped by date and user"""
        condition = (
            and_(
                func.date(ModelLike.time_created) >= date_from,
                func.date(ModelLike.time_created) <= date_to,
            )
            if user_id is None
            else and_(
                func.date(ModelLike.time_created) >= date_from,
                func.date(ModelLike.time_created) <= date_to,
                ModelLike.user_id == user_id,
            )
        )
        query = (
            db.session.query(ModelLike.time_created, func.count(ModelLike.time_created))
            .filter(condition)
            .group_by(ModelLike.time_created)
        )
        return query.all()
