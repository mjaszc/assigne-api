from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    NO_STATUS = "No Status"
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    CANCELLED = "Cancelled"

class TaskBase(BaseModel):
    title: str
    description: str
    status: Status

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class ProjectTasks(TaskBase):
    id: int

    class Config:
        orm_mode = True

class Task(TaskBase):
    status: Status
    id: int

    class Config:
        orm_mode = True