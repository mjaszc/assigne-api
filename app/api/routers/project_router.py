from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

import app.schemas.project_schema as project_schema
import app.crud.project_crud as project_crud
import app.crud.task_crud as task_crud
from app.db.database import SessionLocal
import app.schemas.user_schema as user_schema
import app.crud.user_crud as user_crud
import app.crud.log_crud as log_crud


from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/v1/projects")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=project_schema.Project)
async def create_project(
    project: project_schema.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    # Validation: Due Date property, cannot be earlier than today's date
    if project.due_date < datetime.date.today():
        raise HTTPException(status_code=404, detail="Invalid Due Date property")

    # Generating log to the database
    log_details = f"Created project named {project.name}"
    log_crud.create_log(db, action="Created project", details=log_details)

    return project_crud.create_project(db, project, current_user)

@router.get("/{id}", response_model=project_schema.Project)
async def get_project_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    project = project_crud.get_project(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    assigned_tasks = task_crud.get_assigned_tasks(db, id)

    assigned_users_ids = project_crud.get_assigned_users_id_to_project(db, id)
    assigned_users_list = []
    if assigned_users_ids:
        assigned_users_list = user_crud.get_users_by_ids(db, assigned_users_ids)

    project_response = project_schema.Project(
        id=project.id,
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        due_date=project.due_date,
        author=project.author,
        assigned_tasks=assigned_tasks,
        assigned_users=assigned_users_list
    )

    return project_response

@router.get("/", response_model=List[project_schema.ProjectWithoutTasks])
async def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    return project_crud.get_all_projects(db, skip, limit)


@router.put("/{id}", response_model=project_schema.Project)
async def update_project_by_id(
    id: int,
    project: project_schema.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    project_id = project_crud.get_project(db, id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generating log to the database
    log_details = f"Updated project with ID {id}: New Name: {project.name} | Description: {project.description} | Due Date: {project.due_date}"
    log_crud.create_log(db, action="Updated project", details=log_details)

    return project_crud.update_project(db, id, project)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    project = project_crud.get_project(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generating log to the database
    log_details = f"Deleted project with ID {id}"
    log_crud.create_log(db, action="Deleted project", details=log_details)
    project_crud.delete_project(db, id)

@router.post("/{id}/assign/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assign_user_to_project(
    id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(user_crud.get_current_user),
):
    project_crud.assign_user_to_project(db, id, user_id)

    # Generating log to the database
    log_details = f"Assigned project ID {id} to user ID {user_id} by user {current_user.username}"
    log_crud.create_log(db, action="Assigned project", details=log_details)