from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.user_schema import User
from typing import List
from app.schemas.task_schema import Task

class ProjectBase(BaseModel):
    name: str
    description: Optional[str]



class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    start_date: date
    author: User
    assigned_tasks: Optional[List[Task]] = []

    class Config:
        orm_mode = True
