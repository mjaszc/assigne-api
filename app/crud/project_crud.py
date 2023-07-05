from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exists
from fastapi import HTTPException, status

import app.models.project_model as project_model
import app.schemas.project_schema as project_schema
import app.models.user_model as user_model
import app.schemas.user_schema as user_schema

import datetime


def create_project(db: Session, project: project_schema.ProjectCreate, current_user: user_schema.User):
    # Validation for empty fields
    if not project.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name cannot be empty.")

    if not project.description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project description cannot be empty.")

    if db.query(exists().where(project_model.Project.name == project.name)).scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with the same name already exists.")

    db_project = project_model.Project(
        name=project.name,
        description=project.description,
        start_date=datetime.date.today(),
        due_date=project.due_date,
        author_id=current_user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int):
    return (
        db.query(project_model.Project)
        .filter(project_model.Project.id == project_id)
        .first()
    )


def get_all_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(project_model.Project).offset(skip).limit(limit).all()


def update_project(db: Session, project_id: int, project: project_schema.ProjectUpdate):
    db_project = db.query(project_model.Project).filter_by(id=project_id).first()
    if not db_project:
        return None
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    project = (
        db.query(project_model.Project)
        .filter(project_model.Project.id == project_id)
        .first()
    )
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True

def assign_user_to_project(db: Session, project_id: int, user_id: int):
    project = db.query(project_model.Project).filter(project_model.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found")

    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    project.assigned_users.append(user)
    db.commit()
    return True

def get_assigned_users_id_to_project(db: Session, project_id: int):
    # Getting the the project_id from the associated table to the project table named assigned_users
    project = db.query(project_model.Project).options(joinedload(project_model.Project.assigned_users)).filter(project_model.Project.id == project_id).first()
    if project:
        # Getting id's of users that are assigned to a specified project
        assigned_users_id = [user.id for user in project.assigned_users]        
        return assigned_users_id