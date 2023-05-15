import app.models.user_model as user_model
import app.schemas.user_schema as user_schema
from app.db.database import SessionLocal

from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Optional, Annotated
from dotenv import dotenv_values


config = dotenv_values(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.get("SECRET_KEY"),
        config.get("ALGORITHM"),
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            config.get("SECRET_KEY"),
            config.get("ALGORITHM"),
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
