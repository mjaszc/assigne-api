from pydantic import BaseModel
from datetime import date


class ProjectBase(BaseModel):
    name: str
    description: str | None
    start_date: date


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True
