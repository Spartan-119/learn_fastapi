# here i will create the functions to interact with the DB

from sqlalchemy.orm import Session
from . import  models, schemas
from app.database import SessionLocal

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username = user.username,
        email = user.email,
        password_hash = user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(
        **post.model_dump(),
        author_id = user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int, user_id: int):
    db_comment = models.Comment(
        **comment.model_dump(),
        post_id = post_id,
        author_id = user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment