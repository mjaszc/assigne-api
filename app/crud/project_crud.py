from sqlalchemy.orm import Session

import models.project_model as project_model
import schemas.project_schemas as project_schemas


def create_project(db: Session, project: project_schemas.ProjectCreate):
    db_item = project_model.Project(**project.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_project_by_id(db: Session, project_id: int):
    return (
        db.query(project_model.Project)
        .filter(project_model.Project.id == project_id)
        .first()
    )


def get_all_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(project_model.Project).offset(skip).limit(limit).all()
