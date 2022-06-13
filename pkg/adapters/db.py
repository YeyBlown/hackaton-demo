# TODO: ensure thread safe
# TODO: should i move to DBFacade?
# TODO: handle exceptions (already liked, not exists...)
# TODO: create like instance in different database
import datetime
from typing import Optional

from fastapi_sqlalchemy import db
from sqlalchemy import and_, func

from adapters.hash_utils import HashUtils
from entities.exceptions import PostAlreadyLikedException, PostIsNotLikedException
from models.models import User as ModelUser
from models.models import Post as ModelPost
from models.models import Like as ModelLike

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
    def add_post_created(user: ModelUser, post: ModelPost):
        user.posts_created.append(post)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def create_user(user: SchemaUser):
        password = user.hashed_password
        hashed_password = HashUtils.get_password_hash(password)
        db_user = ModelUser(
            username=user.username,
            hashed_password=hashed_password,
            posts_created=[],
            likes=[],
        )
        db.session.add(db_user)
        db.session.commit()
        return db_user

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
        db_post = ModelPost(
            header=post.header, content=post.content, author_id=post.author_id
        )
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

    @staticmethod
    def get_posts_by_user_date(
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        user_id: Optional[int] = None,
    ):
        # TODO: refactor prettier
        if user_id is not None:
            query = db.session.query(ModelPost).filter(
                and_(
                    func.date(ModelPost.time_created) >= date_from,
                    func.date(ModelPost.time_created) <= date_to,
                    ModelPost.author_id == user_id,
                )
            )
        else:
            query = db.session.query(ModelPost).filter(
                and_(
                    func.date(ModelPost.time_created) >= date_from,
                    func.date(ModelPost.time_created) <= date_to,
                )
            )
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
        db_like = ModelLike(
            user_id=user.id,
            post_id=post.id,
            user=user,
            post=post
        )
        db.session.add(db_like)
        db.session.commit()
        UserDBAdapter._add_like(user, db_like)
        PostDBAdapter._add_like(post, db_like)
        db.session.commit()
        return db_like

    @staticmethod
    def remove(user: ModelUser, post: ModelPost):
        like = LikeDBAdapter.get_like(user.id, post.id)
        if not like:
            raise PostIsNotLikedException()

        UserDBAdapter._remove_like(user, like)
        PostDBAdapter._remove_like(post, like)

        db.session.query(ModelLike).filter(and_(
            ModelLike.id == like.id,
            ModelLike.post_id == post.id
        )).delete()

    @staticmethod
    def is_like_exists(user_id: id, post_id: id):
        like = db.session.query(ModelLike).filter(
            and_(
                ModelLike.user_id == user_id,
                ModelLike.post_id == post_id
            )
        ).first()
        return like

    @staticmethod
    def get_like(user_id: id, post_id: id):
        like = db.session.query(ModelLike).filter(
            and_(
                ModelLike.user_id == user_id,
                ModelLike.post_id == post_id
            )
        ).first()
        return like