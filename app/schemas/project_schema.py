from pydantic import BaseModel
from typing import Optional
from datetime import date
from typing import List
from app.schemas.task_schema import Task
from app.schemas.user_schema import User, UserWithoutTasks

class ProjectBase(BaseModel):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    due_date: Optional[date]


class ProjectUpdate(ProjectBase):
    pass

class ProjectWithoutTasks(ProjectBase):
    id: int
    start_date: date
    due_date: Optional[date]
    author: User

    class Config:
        orm_mode = True

class Project(ProjectBase):
    id: int
    start_date: date
    due_date: Optional[date]
    author: UserWithoutTasks
    assigned_tasks: Optional[List[Task]] = []
    assigned_users: Optional[List[UserWithoutTasks]] = []

    class Config:
        orm_mode = True
