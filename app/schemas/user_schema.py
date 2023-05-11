from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: Optional[str]


class User(UserBase):
    id: int
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
