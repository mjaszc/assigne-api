from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
from app.db.database import SessionLocal


router = APIRouter(prefix="/api/v1/users")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=user_schema.User)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    users = user_crud.get_all_users(db, skip, limit)
    return users


@router.get("/{id}", response_model=user_schema.User)
async def get_project_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    user = user_crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
