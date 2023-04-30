from pydantic import BaseModel
from datetime import date


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: date


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True
