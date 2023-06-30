from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.task_schema as task_schema
import app.crud.task_crud as task_crud
from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud

router = APIRouter(prefix="/api/v1/projects/{project_id}/tasks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=task_schema.Task)
async def create_task(
    task: task_schema.TaskCreate,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    return task_crud.create_task(db, task, project_id)

@router.get("/{task_id}", response_model=task_schema.Task)
async def get_task_by_id(
    task_id: int,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    task = task_crud.get_task_by_id(db, task_id, project_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=task_schema.Task)
async def update_task_by_id(
    task_id: int,
    task: task_schema.TaskBase,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    get_task = task_crud.get_task_by_id(db, id, project_id)
    if get_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = task_crud.update_task(db, id, task, project_id)
    return updated_task

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    id: int,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    task_to_delete = task_crud.get_task_by_id(db, id, project_id)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_crud.delete_task(db, id, project_id)

@router.post("/{task_id}/assign/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assign_task_to_user(
    id: int,
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    task_crud.assign_user_to_task(db, id, project_id, user_id)