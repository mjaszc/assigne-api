from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.comment_schema import Comment


class DiscussionBase(BaseModel):
    title: str
    description: str

class DiscussionCreate(DiscussionBase):
    pass

class Discussion(DiscussionBase):
    id: int
    project_id: int
    user_id: int
    created_at: date
    comments: Optional[List[Comment]] = []

    class Config:
        orm_mode = True