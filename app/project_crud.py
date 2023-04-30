from sqlalchemy.orm import Session

import models
import schemas


def create_project(db: Session, project: schemas.ProjectCreate):
    db_item = models.Project(**project.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_all_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()
