from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Status(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    CANCELLED = "Cancelled"

class TaskBase(BaseModel):
    title: str
    description: str



class TaskCreate(TaskBase):
    status: Optional[Status]

class ProjectTasks(TaskBase):
    id: int

    class Config:
        orm_mode = True

class Task(TaskBase):
    status: Optional[Status]
    id: int

    class Config:
        orm_mode = True