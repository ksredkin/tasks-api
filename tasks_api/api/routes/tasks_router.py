from fastapi import APIRouter, Depends, HTTPException, status
from tasks_api.services.auth_service import AuthService
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.orm_task_repository import OrmTaskRepository
from tasks_api.repositories.orm_user_repository import OrmUserRepository
from tasks_api.models.schemas import TaskCreate, TaskResponse, TaskUpdate

tasks_router = APIRouter(prefix="/tasks")

@tasks_router.get("/", status_code=200, response_model=list[TaskResponse])
def get_tasks(user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        tasks = OrmTaskRepository.get_user_tasks(user_id)
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
        task = OrmTaskRepository.create_task(user_id, task.name, task.text, task.state)
        
        if not task:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create task")
        
        return task
    
    except HTTPException:
        raise

@tasks_router.put("/{task_id}", response_model=TaskResponse, status_code=200)
def update_task(task_id: int, task_data: TaskUpdate, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        update_kwargs = {k: v for k, v in task_data.dict().items() if v is not None}
        task = OrmTaskRepository.update_task(user_id, task_id, **update_kwargs)
        
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