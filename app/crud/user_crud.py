from sqlalchemy.orm import Session
import app.models.user_model as user_model
import app.schemas.user_schema as user_schema
from passlib.context import CryptContext
from sqlalchemy import or_


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: user_schema.UserCreate):
    password = pwd_context.hash(user.password)
    db_user = user_model.User(
        username=user.username, email=user.email, password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, email: str, username: str):
    return (
        db.query(user_model.User)
        .filter(
            or_(
                user_model.User.email == email,
                user_model.User.username == username,
            )
        )
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return (
        db.query(user_model.User).filter(user_model.User.username == username).first()
    )
