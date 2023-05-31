from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas.task_schema as task_schema
import app.crud.task_crud as task_crud
from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud

from typing import List

router = APIRouter(prefix="/api/v1/projects/{project_id}/tasks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=task_schema.Task)
async def create_task_for_the_project(
    task: task_schema.TaskCreate,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    return task_crud.create_task(db, task, project_id)


@router.get("/", response_model=List[task_schema.ProjectTasks])
def get_assigned_tasks_for_the_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    assigned_tasks = task_crud.get_assigned_tasks(db, project_id)
    return assigned_tasks