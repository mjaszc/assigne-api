from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.user_schema import User


class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    start_date: date


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    author: User

    class Config:
        orm_mode = True
