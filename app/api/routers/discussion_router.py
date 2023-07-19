from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
import app.crud.discussion_crud as discussion_crud
import app.schemas.discussion_schema as discussion_schema
import app.crud.project_crud as project_crud


router = APIRouter(prefix="/api/v1/projects/{project_id}/discussions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=discussion_schema.Discussion)
async def create_discussion(
    discussion: discussion_schema.DiscussionCreate,
    project_id:int,
    user_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    # Validations
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return discussion_crud.create_discussion(db, discussion, current_user, project_id)

@router.get("/{discussion_id}", response_model=discussion_schema.Discussion)
async def get_task_discussion(
    discussion_id: int,
    task_id:int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_task_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    return discussion

@router.put("/{discussion_id}", response_model=discussion_schema.Discussion)
async def update_task_discussion(
    discussion: discussion_schema.DiscussionBase,
    discussion_id: int,
    task_id:int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_task_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    return discussion_crud.update_discussion(db, discussion, discussion_id, current_user.id)

@router.delete("/{discussion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_discussion(
    discussion_id: int,
    task_id:int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_task_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    discussion_crud.delete_discussion(db, discussion_id)