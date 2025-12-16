from fastapi import APIRouter, status
from tasks_api.models.user_register import UserRegister
from tasks_api.models.user_login import UserLogin
from tasks_api.services.user_service import UserService
from tasks_api.utils.response_factory import ResponseFactory

user_router = APIRouter(prefix="/user")

@user_router.post("/register")
def register(user_register: UserRegister):
    is_succes = UserService.create_new_user(user_register.login, user_register.password)
    if is_succes is False:
        raise ResponseFactory.error_response(detail="Username already exists")
    return ResponseFactory.succes_response(message="User registered successfully")

@user_router.post("/login")
def login(user_login: UserLogin):
    token = UserService.login(user_login.login, user_login.password)
    if token is None:
        raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return ResponseFactory.succes_response(data={"access_token": token, "token_type": "bearer"})