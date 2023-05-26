from sqlalchemy.orm import Session

import app.models.project_model as project_model
import app.schemas.project_schema as project_schema
import app.schemas.user_schema as user_schema

from datetime import datetime


def create_project(db: Session, project: project_schema.ProjectCreate, current_user_id: user_schema.User):
    db_item = project_model.Project(
        name=project.name,
        description=project.description,
        start_date=datetime.utcnow(),
        author_id=current_user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
