from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    content = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey('user.id'))

    likes = relationship("User", back_populates="post")  # TODO: review it works properly, configure deletes
    author = relationship('User')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = String(String)  # TODO: change to hashes
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    time_last_login = Column(DateTime(timezone=True), onupdate=func.now())

    likes = relationship("Post", back_populates="user")  # TODO: review it works properly, configure deletes
