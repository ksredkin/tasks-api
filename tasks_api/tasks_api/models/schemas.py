from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ApiKeyRequest(BaseModel):
    api_key: str

class UserBase(BaseModel):
    login: str = Field(min_length=3, max_length=32, description="Логин от 3 до 32 символов")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64, description="Пароль от 8 до 64 символов")

class UserLogin(UserBase):
    password: str = Field(min_length=8, max_length=64, description="Пароль от 8 до 64 символов")

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    name: str
    text: str
    state: Optional[str] = "Active"
    due_date: Optional[datetime] = None
    visible_from: Optional[datetime] = None
    recurrence_type: Optional[str] = None
    recurrence_day_of_week: Optional[int] = None
    recurrence_month_day: Optional[int] = None
    folder_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: str
    text: str = None
    state: str = None
    due_date: Optional[datetime] = None
    visible_from: Optional[datetime] = None
    recurrence_type: Optional[str] = None
    recurrence_day_of_week: Optional[int] = None
    recurrence_month_day: Optional[int] = None
    folder_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    due_date: Optional[datetime] = None
    visible_from: Optional[datetime] = None
    user_id: int
    folder_id: Optional[int]
    recurrence_type: Optional[str] = None
    recurrence_day_of_week: Optional[int] = None
    recurrence_month_day: Optional[int] = None
    next_run: Optional[datetime]
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