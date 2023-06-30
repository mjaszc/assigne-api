from sqlalchemy.orm import Session
from fastapi import HTTPException

import app.models.task_model as task_model
import app.schemas.task_schema as task_schema
import app.schemas.project_schema as project_schema
import app.models.user_model as user_model


def create_task(db: Session, task: task_schema.TaskCreate, current_project: project_schema.Project):
    db_task = task_model.Task(
        title=task.title,
        description=task.description,
        project_id=current_project
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_assigned_tasks(db: Session, project_id: int):
    assigned_tasks = db.query(task_model.Task).filter(task_model.Task.project_id == project_id).all()
    return assigned_tasks

def get_task_by_id(db: Session, task_id: int, project_id: int):
    return (
        db.query(task_model.Task)
        .filter(task_model.Task.id == task_id, task_model.Task.project_id == project_id)
        .first()
    )

def update_task(db: Session, task_id: int, task: task_schema.TaskBase, project_id: int):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.project_id == project_id).first()
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, project_id: int):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.project_id == project_id).first()
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True

def assign_user_to_task(db: Session, task_id: int, project_id: int, user_id: int):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.project_id == project_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    db_task.assigned_user.append(user)
    db.commit()
    return True
