from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.services.user_service import UserService
from fastapi import APIRouter, status, HTTPException
from tasks_api.models.schemas import UserCreate, UserResponse, UserLogin

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
def login(user_login: UserLogin):
    try:
        token = UserService.login(user_login.login, user_login.password)
        if token is None:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        return ResponseFactory.success_response(data={"access_token": token, "token_type": "bearer"})
    
    except HTTPException:
        raise