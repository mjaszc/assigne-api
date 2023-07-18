from sqlalchemy.orm import Session
import datetime

import app.schemas.task_schema as task_schema
import app.schemas.project_schema as project_schema
import app.schemas.user_schema as user_schema
import app.models.discussion_model as discussion_model
import app.schemas.discussion_schema as discussion_schema

def create_discussion(db: Session, discussion: discussion_schema.Discussion, user: user_schema.User, task: task_schema.Task, project: project_schema.Project):
    new_discussion = discussion_model.Discussion(
        task_id=task,
        project_id=project,
        user_id=user.id,
        message=discussion.message,
        created_at=datetime.date.today()
    )
    db.add(new_discussion)
    db.commit()
    db.refresh(new_discussion)

    return new_discussion

def get_task_discussion(db: Session, discussion_id: int):
    return (
        db.query(discussion_model.Discussion)
        .filter(discussion_model.Discussion.id == discussion_id)
        .first()
    )

def update_discussion(db: Session, discussion: discussion_schema.Discussion, discussion_id: int, user_id: int):
    db_disc = db.query(discussion_model.Discussion).filter(discussion_model.Discussion.id == discussion_id).first()
    if not db_disc:
        return None
    for key, value in discussion.dict(exclude_unset=True).items():
        setattr(db_disc, key, value)
    db.add(db_disc)
    db.commit()
    db.refresh(db_disc)
    return db_disc

def delete_discussion(db: Session, discussion_id: int):
    db_disc = db.query(discussion_model.Discussion).filter(discussion_model.Discussion.id == discussion_id).first()
    if not db_disc:
        return False
    db.delete(db_disc)
    db.commit()
    return True