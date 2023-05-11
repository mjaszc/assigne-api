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
    # Check if user already exists
    existing_user = user_crud.get_user(db, user.email, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already registered",
        )

    db_user = user_crud.create_user(db, user)
    return db_user


@router.post("/login", response_model=user_schema.User)
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify password
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return db_user
