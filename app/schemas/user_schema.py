from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.schemas.task_schema import Task

# USER
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    password: Optional[str]


class User(UserBase):
    is_active: Optional[bool]
    id: int
    assigned_tasks: Optional[List[Task]] = []

    class Config:
        orm_mode = True

# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]

