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
    state: Optional[str] = "Active"
    folder_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: str = None
    text: str = None
    state: str = None
    due_date: datetime = None
    folder_id: int = None

class TaskResponse(TaskBase):
    id: int
    date: datetime
    user_id: int
    folder_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None
    show_progress: Optional[bool] = False

class FolderResponse(BaseModel):
    id: int
    user_id: int
    name: str
    parent_id: Optional[int]
    show_progress: Optional[bool]
    model_config = ConfigDict(from_attributes=True)