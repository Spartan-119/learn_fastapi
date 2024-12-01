# here i will define the models (tables)

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index = True)
    email = Column(String, unique = True, index = True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default = False)

    posts = relationship("Post", back_populates = "author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    content = Column(Text)
    created_at = Column(DateTime, default = datetime.now)
    author_id = Column(Integer, ForeignKey("users.id"))

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key = True, index = True)
    content = Column(Text)
    created_at = Column(DateTime, default = datetime.now)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates = "comments")
    author = relationship("User")