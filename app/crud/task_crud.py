from sqlalchemy.orm import Session

import app.models.task_model as task_model
import app.schemas.task_schema as task_schema
import app.schemas.project_schema as project_schema


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