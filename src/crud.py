from sqlalchemy.orm import Session

import models
import schemas


def create_project_item(db: Session, project: schemas.ProjectCreate):
    db_item = models.Project(**project.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
