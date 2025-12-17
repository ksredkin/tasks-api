from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.models.user_register import UserRegister
from tasks_api.services.user_service import UserService
from fastapi import APIRouter, status, HTTPException
from tasks_api.models.user_login import UserLogin

user_router = APIRouter(prefix="/user")

@user_router.post("/register")
def register(user_register: UserRegister):
    try:
        is_succes = UserService.create_new_user(user_register.login, user_register.password)
        if is_succes is False:
            raise ResponseFactory.error_response(detail="Username already exists")
        return ResponseFactory.success_response(message="User registered successfully")

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