from sqlalchemy.orm import Session
from sqlalchemy import exists
from fastapi import HTTPException

import app.models.project_model as project_model
import app.models.user_model as user_model
import app.schemas.project_schema as project_schema

from datetime import datetime


def create_project(db: Session, project: project_schema.ProjectCreate, user_id: int):
    if db.query(exists().where(project_model.Project.name == project.name)).scalar():
        raise HTTPException(status_code=400, detail="Project with the same name already exists.")

    db_project = project_model.Project(
        name=project.name,
        description=project.description,
        start_date=datetime.utcnow(),
        author_id=user_id
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
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    project.assigned_users.append(user)
    db.commit()
    return True