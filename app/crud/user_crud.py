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
from typing import Optional, Annotated, List
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


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[user_model.User]:
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_users_by_ids(db: Session, user_ids: List[int]):
    users = db.query(user_model.User).filter(user_model.User.id.in_(user_ids)).all()
    return users


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

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.get("SECRET_KEY"), config.get("ALGORITHM"))
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.get("SECRET_KEY"), config.get("ALGORITHM"))
        username = payload.get("sub")
        if username is None:
            raise JWTError()
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

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
