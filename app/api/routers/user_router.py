from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
from app.db.database import SessionLocal


router = APIRouter(prefix="/api/v1")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = user_crud.get_user(db=db, email=user.email, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already registered",
        )

    # hash the password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    db_user = user_crud.create_user(db=db, user=user)
    return db_user
