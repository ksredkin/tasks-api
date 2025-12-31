from fastapi import APIRouter, Depends, HTTPException, status
from tasks_api.services.auth_service import AuthService
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.tasks_repository import TasksRepository
from tasks_api.repositories.user_repository import UserRepository
from tasks_api.models.task import Task

tasks_router = APIRouter(prefix="/tasks")

@tasks_router.get("/")
def get_tasks(user_id: int = Depends(AuthService(UserRepository).get_current_user)):
    try:
        user_tasks = TasksRepository.get_user_tasks(user_id)
        tasks_list = []
        if user_tasks:
            for task in user_tasks:
                tasks_list.append({"id": task[0], "name": task[1], "text": task[2], "state": task[3], "date": task[4]})

        return ResponseFactory.success_response(data={"tasks": tasks_list})
    
    except HTTPException:
        raise

@tasks_router.get("/{id}")
def get_task(id: int, user_id: int = Depends(AuthService(UserRepository).get_current_user)):
    try:
        task = TasksRepository.get_user_task(id, user_id)

        if not task:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return ResponseFactory.success_response(data={"task": {"id": id, "name": task[0], "text": task[1], "state": task[2], "date": task[3]}})
    
    except HTTPException:
        raise

@tasks_router.post("/")
def create_task(task: Task, user_id: int = Depends(AuthService(UserRepository).get_current_user)):
    try:
        id, date = TasksRepository.create_task(user_id, task.name, task.text, task.state)
        return ResponseFactory.success_response(status.HTTP_201_CREATED, "Task added successfully", {"task": {"id": id, "name": task.name, "text": task.text, "state": task.state, "date": date}})
    
    except HTTPException:
        raise

@tasks_router.put("/{task_id}")
def update_task(task_id: int, task: Task, user_id: int = Depends(AuthService(UserRepository).get_current_user)):
    try:
        date = TasksRepository.update_task(user_id, task_id, task.name, task.text, task.state)
        
        if not date:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Task not found")

        return ResponseFactory.success_response(status.HTTP_200_OK, "Task updated successfully", {"task": {"id": task_id, "name": task.name, "text": task.text, "state": task.state, "date": date}})
    
    except HTTPException:
        raise

@tasks_router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(AuthService(UserRepository).get_current_user)):
    try:
        task = TasksRepository.delete_task(user_id, task_id)
        
        if task is None:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Task not found")

        return ResponseFactory.success_response(status.HTTP_200_OK, "Task deleted successfully", {"task": {"id": task_id, "name": task[0], "text": task[1], "state": task[2], "date": task[3]}})
    
    except HTTPException:
        raise