from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
from app.db.database import SessionLocal


router = APIRouter(prefix="/api/v1")


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
