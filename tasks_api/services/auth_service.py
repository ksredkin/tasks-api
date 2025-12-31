from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status
from tasks_api.utils.jwt import JWTManager
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.user_repository import UserRepository

security = HTTPBearer()

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @classmethod
    def get_current_user(cls, credentials: HTTPAuthorizationCredentials = Depends(security)) -> int | None:
        """Извлекает id из jwt токена"""
        token = credentials.credentials
        payload = JWTManager.decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        
        user = UserRepository.get_user_login(user_id)
        
        if not user:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid user ID in token")
            
        return int(user_id)