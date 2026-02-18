from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.services.user_service import UserService
from fastapi import APIRouter, status, HTTPException, Request
from tasks_api.models.schemas import UserCreate, UserResponse, UserLogin
from tasks_api.utils.attempts_storage import AttemptsStorage
from tasks_api.core.config import MAX_ATTEMPTS_TO_LOGIN

user_router = APIRouter(prefix="/user")

@user_router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate):
    try:
        user = UserService.create_new_user(user_data.login, user_data.password)
        if user is None:
            raise ResponseFactory.error_response(detail="Username already exists")
        return user

    except HTTPException:
        raise

@user_router.post("/login")
def login(request: Request, user_login: UserLogin):
    try:
        storage = AttemptsStorage()

        if storage.get_attempts(request.client.host, user_login.login) > MAX_ATTEMPTS_TO_LOGIN:
            raise HTTPException(429, "Too many login attempts")

        token = UserService.login(user_login.login, user_login.password)
        
        if token is None:
            storage.add_attempt(request.client.host, user_login.login)
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        
        storage.reset_attempts(request.client.host, user_login.login)
        return ResponseFactory.success_response(data={"access_token": token, "token_type": "bearer"})
    
    except HTTPException:
        raise