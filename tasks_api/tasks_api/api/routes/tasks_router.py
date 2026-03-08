from fastapi import APIRouter, Depends, HTTPException, status
from tasks_api.services.auth_service import AuthService
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.orm_task_repository import OrmTaskRepository
from tasks_api.repositories.orm_user_repository import OrmUserRepository
from tasks_api.models.schemas import TaskCreate, TaskResponse, TaskUpdate, ApiKeyRequest
from tasks_api.utils.env_config import EnvConfig

tasks_router = APIRouter(prefix="/tasks")

@tasks_router.get("/", status_code=200, response_model=list[TaskResponse])
def get_tasks(user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        tasks = OrmTaskRepository.get_user_tasks(user_id)
        return tasks or []
    
    except HTTPException:
        raise

@tasks_router.get("/stats", status_code=200)
def get_tasks_stats(user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        stats = OrmTaskRepository.get_tasks_stats(user_id)
        return stats or {}
    
    except HTTPException:
        raise

@tasks_router.get("/today", status_code=200, response_model=list[TaskResponse])
def get_tasks_today(user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        tasks = OrmTaskRepository.get_user_tasks_today(user_id)
        return tasks or []
    
    except HTTPException:
        raise

@tasks_router.get("/{id}", status_code=200, response_model=TaskResponse)
def get_task(id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        task = OrmTaskRepository.get_user_task_by_id(user_id, id)

        if not task:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return task
    
    except HTTPException:
        raise

@tasks_router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        task = OrmTaskRepository.create_task(user_id, task.name, task.text, task.state, task.folder_id, task.recurrence_type, task.recurrence_day_of_week, task.recurrence_month_day, task.due_date, task.visible_from)
        
        if not task:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create task")
        
        return task
    
    except HTTPException:
        raise

@tasks_router.put("/{task_id}", response_model=TaskResponse, status_code=200)
def update_task(task_id: int, task_data: TaskUpdate, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        task = OrmTaskRepository.update_task(user_id, task_id, task_data.name, task_data.text, task_data.state, task_data.folder_id, task_data.recurrence_type, task_data.recurrence_day_of_week, task_data.recurrence_month_day, task_data.due_date, task_data.visible_from)
        
        if not task:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Task not found")

        return task
    
    except HTTPException:
        raise

@tasks_router.delete("/{task_id}", status_code=200, response_model=TaskResponse)
def delete_task(task_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        task = OrmTaskRepository.delete_task(user_id, task_id)
        
        if task is None:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Task not found")

        return task
    
    except HTTPException:
        raise

@tasks_router.post("/repeat", status_code=200)
def update_repeat_tasks(request: ApiKeyRequest):
    try:
        config = EnvConfig()

        if not request.api_key == config.get_api_key():
            raise ResponseFactory.error_response(status.HTTP_400_BAD_REQUEST, "Invalid api_key")

        OrmTaskRepository.update_repeat_tasks()

        return {"status": "success"}

    except HTTPException:
        raise