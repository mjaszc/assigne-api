from pydantic import BaseModel
from datetime import date

class CommentBase(BaseModel):
    message: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    discussion_id: int
    user_id: int
    created_at: date

    class Config:
        orm_mode = True