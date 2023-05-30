from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas.task_schema as task_schema
import app.crud.task_crud as task_crud
from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud

router = APIRouter(prefix="/api/v1/tasks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=task_schema.Task)
async def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    return task_crud.create_task(db, task)