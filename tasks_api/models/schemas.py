from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    login: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    name: str
    text: str
    state: str = "Active"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    state: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    date: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)