from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status
from tasks_api.utils.jwt import JWTManager
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.orm_user_repository import OrmUserRepository

security = HTTPBearer()

class AuthService:
    def __init__(self, user_repo: OrmUserRepository):
        self.user_repo = user_repo

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> int | None:
        """Извлекает id из jwt токена"""
        token = credentials.credentials
        payload = JWTManager.decode_token(token)
        user_id = int(payload.get("sub"))

        if user_id is None:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        
        user = await self.user_repo.get_user_by_id(user_id)
        
        if not user:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid user ID in token")
            
        return user.id
    
    async def _get_user_id_from_token(self, token: str) -> int | None:
        """Извлекает id из jwt токена"""
        payload = JWTManager.decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        
        user = await self.user_repo.get_user_by_id(user_id)
        
        if not user:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid user ID in token")
            
        return user.id