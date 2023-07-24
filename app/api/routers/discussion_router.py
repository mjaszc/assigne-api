from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
import app.crud.discussion_crud as discussion_crud
import app.schemas.discussion_schema as discussion_schema
import app.schemas.comment_schema as comment_schema
import app.crud.comment_crud as comment_crud
import app.crud.project_crud as project_crud
import app.crud.log_crud as log_crud



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
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    # Validations
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Generating log to the database
    log_details = f"Created discussion: {discussion.message} by user {current_user.username}"
    log_crud.create_log(db, action="Created discussion", details=log_details)

    return discussion_crud.create_discussion(db, discussion, current_user, project_id)

@router.get("/{discussion_id}", response_model=discussion_schema.Discussion)
async def get_discussion(
    discussion_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    # Retrieving all comments for a discussion
    discussion_comments = comment_crud.get_discussion_comments(db, discussion_id)

    discussion_response = discussion_schema.Discussion(
        id=discussion.id,
        message=discussion.message,
        project_id=discussion.project_id,
        user_id=discussion.user_id,
        created_at=discussion.created_at,
        comments=discussion_comments
    )

    return discussion_response

@router.put("/{discussion_id}", response_model=discussion_schema.Discussion)
async def update_discussion(
    discussion: discussion_schema.DiscussionBase,
    discussion_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    # Generating log to the database
    log_details = f"Updated discussion with ID {id}: New Message: {discussion.message}"
    log_crud.create_log(db, action="Updated discussion", details=log_details)

    return discussion_crud.update_discussion(db, discussion, discussion_id, current_user.id)

@router.delete("/{discussion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_discussion(
    discussion_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    # Generating log to the database
    log_details = f"Deleted discussion with ID {discussion_id} in project ID {project_id}"
    log_crud.create_log(db, action="Deleted discussion", details=log_details)

    discussion_crud.delete_discussion(db, discussion_id)

@router.post("/{discussion_id}/comments", response_model=comment_schema.Comment)
def create_comment(
    discussion_id: int,
    project_id: int,
    comment: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    # Generating log to the database
    log_details = f"Created comment: {comment.message} by user {current_user.username}"
    log_crud.create_log(db, action="Created comment", details=log_details)

    return comment_crud.create_comment(db, discussion_id, comment, current_user)

@router.get("/{discussion_id}/comments/{comment_id}", response_model=comment_schema.Comment)
async def get_comment(
    discussion_id: int,
    comment_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    comment = comment_crud.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    return comment

@router.put("/{discussion_id}/comments/{comment_id}", response_model=comment_schema.Comment)
async def update_comment(
    comment: comment_schema.CommentBase,
    comment_id: int,
    discussion_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    comment = comment_crud. get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Generating log to the database
    log_details = f"Updated comment: New Message: {comment.message}"
    log_crud.create_log(db, action="Updated comment", details=log_details)

    return discussion_crud.update_discussion(db, comment, comment_id, current_user.id)

@router.delete("/{discussion_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    discussion_id: int,
    project_id:int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user)
):
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    discussion = discussion_crud.get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")

    comment = comment_crud.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Generating log to the database
    log_details = f"Deleted comment with ID {comment_id}"
    log_crud.create_log(db, action="Deleted comment", details=log_details)

    comment_crud.delete_comment(db, comment_id)