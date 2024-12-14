from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: int
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: int = 1
    due_date: Optional[datetime] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[int]
    due_date: Optional[datetime]


class LoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    token: str
