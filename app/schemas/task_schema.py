from pydantic import BaseModel
from app.schemas.project_schema import Project

class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    project: Project

    class Config:
        orm_mode = True