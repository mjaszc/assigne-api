from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
from app.db.database import SessionLocal

from typing import List


router = APIRouter(prefix="/api/v1/users")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[user_schema.User])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    users = user_crud.get_all_users(db, skip, limit)
    return users
