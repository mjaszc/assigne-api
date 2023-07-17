from pydantic import BaseModel
from datetime import date

class DiscussionBase(BaseModel):
    message: str

class DiscussionCreate(DiscussionBase):
    pass

class Discussion(DiscussionBase):
    id: int
    task_id: int
    project_id: int
    user_id: int
    created_at: date

    class Config:
        orm_mode = True