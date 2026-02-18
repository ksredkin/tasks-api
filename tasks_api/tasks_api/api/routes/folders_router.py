from tasks_api.models.schemas import FolderCreate
from fastapi import APIRouter, Depends, status, Query
from tasks_api.services.auth_service import AuthService
from tasks_api.repositories.orm_user_repository import OrmUserRepository
from tasks_api.repositories.orm_folder_repository import OrmFolderRepository
from tasks_api.repositories.orm_task_repository import OrmTaskRepository
from tasks_api.models.schemas import FolderResponse, TaskResponse
from tasks_api.utils.response_factory import ResponseFactory
from typing import Optional

folders_router = APIRouter(prefix="/folders")

@folders_router.get("/", response_model=list[FolderResponse])
def get_folders(user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        folders = OrmFolderRepository.get_user_folders(user_id) 
        return folders if folders else []

    except Exception:
        raise

@folders_router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(folder_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        folder = OrmFolderRepository.get_user_folder(user_id, folder_id)

        if not folder:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return folder
    
    except Exception:
        raise

@folders_router.get("/{folder_id}/tasks", response_model=list[TaskResponse])
def get_folder_tasks(folder_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        tasks = OrmTaskRepository.get_user_tasks_in_folder(user_id, folder_id if folder_id != 0 else None)

        if tasks is None:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return tasks
    
    except Exception:
        raise

@folders_router.get("/{folder_id}/folders", response_model=list[FolderResponse])
def get_folder_folders(folder_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        folders = OrmFolderRepository.get_user_folders_in_folder(user_id, folder_id if folder_id != 0 else None)

        if folders is None:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return folders
    
    except Exception:
        raise

@folders_router.get("/{folder_id}/progress")
def get_folder_folders(folder_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        progress = OrmFolderRepository.get_folder_progress(user_id, folder_id)

        if progress is None:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")

        return {"user_id": user_id, "folder_id": folder_id, "progress": progress}
    
    except Exception:
        raise

@folders_router.post("/", response_model=FolderResponse, status_code=201)
def create_folder(folder: FolderCreate, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        return OrmFolderRepository.create_folder(user_id, folder.name, folder.parent_id, folder.show_progress)

    except Exception:
        raise

@folders_router.put("/{folder_id}", response_model=FolderResponse, status_code=201)
def update_folder(folder_id: int, folder: FolderCreate, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        folder = OrmFolderRepository.update_folder(user_id, folder_id, folder.name, folder.parent_id, folder.show_progress)

        if not folder:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")
        
        return folder

    except Exception:
        raise

@folders_router.delete("/{folder_id}", response_model=FolderResponse, status_code=201)
def delete_folder(folder_id: int, user_id: int = Depends(AuthService(OrmUserRepository).get_current_user)):
    try:
        folder = OrmFolderRepository.delete_folder(user_id, folder_id)

        if not folder:
            raise ResponseFactory.error_response(status.HTTP_404_NOT_FOUND, "Not found")
        
        return folder

    except Exception:
        raise