from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


# association_table = Table(
#     "association",
#     Base.metadata,
#     Column("post_id", ForeignKey("post.id")),
#     Column("user_id", ForeignKey("user.id")),
# )


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    content = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="posts_created")

    likes = relationship(
        "Like", back_populates="post"
    )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    time_last_login = Column(DateTime(timezone=True), onupdate=func.now())

    posts_created = relationship("Post", back_populates="author")

    likes = relationship(
        "Like", back_populates="user"
    )  # TODO: review it works properly, configure deletes


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="likes")

    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="likes")
