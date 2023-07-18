from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.task_schema as task_schema
from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.task_crud as task_crud
import app.crud.user_crud as user_crud
import app.crud.project_crud as project_crud
import app.schemas.discussion_schema as discussion_schema

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
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=task_schema.Task)
async def update_task_by_id(
    task_id: int,
    task: task_schema.TaskBase,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    get_task = task_crud.get_task_by_id(db, task_id, project_id)
    if get_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task_crud.update_task(db, task_id, task, project_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    task_to_delete = task_crud.get_task_by_id(db, id, project_id)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_crud.delete_task(db, task_id, project_id)

@router.post("/{task_id}/assign/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assign_task_to_user(
    task_id: int,
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    task_crud.assign_user_to_task(db, task_id, project_id, user_id)\

@router.post("/{task_id}/discussions", response_model=discussion_schema.Discussion)
async def create_discussion(
    discussion: discussion_schema.DiscussionCreate,
    task_id:int,
    project_id:int,
    user_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    return task_crud.create_discussion(db, discussion, current_user, task_id, project_id)

@router.get("/{task_id}/discussions/{discussion_id}", response_model=discussion_schema.Discussion)
async def get_task_discussion(
    discussion_id: int,
    task_id:int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    return task_crud.get_task_discussion(db, discussion_id)

@router.delete("/{task_id}/discussions/{discussion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_discussion(
    discussion_id: int,
    task_id:int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    task_crud.delete_discussion(db, discussion_id)