from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from tasks_api.core.config import JWT_EXPIRATION_TIME, JWT_ALGORITHM
from datetime import datetime, timezone, timedelta
from fastapi import Depends, status
from jose import jwt, JWTError
from tasks_api.utils.response_factory import ResponseFactory
from tasks_api.repositories.user_repository import UserRepository

class JWTManager:
    """Класс для работы с jwt"""
    _security = HTTPBearer()
    _secret_key = None

    @classmethod
    def set_secret_key(cls, secret_key: str):
        if cls._secret_key is None:
            cls._secret_key = secret_key

    @classmethod
    def get_user_id_from_jwt(cls, credentials: HTTPAuthorizationCredentials = Depends(_security)) -> int | None:
        """Извлекает id из jwt токена"""
        try:
            token = credentials.credentials
            payload = jwt.decode(token, cls._secret_key, algorithms=JWT_ALGORITHM)
            user_id = payload.get("sub")

            if user_id is None:
                raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid token")
            
            user = UserRepository.get_user_login(user_id)
            
            if not user:
                raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "User not found")
            
            return int(user_id)
        except ValueError:
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid user ID in token")

        except JWTError as e:
            print(f"Ошибка JWT: {e}")
            raise ResponseFactory.error_response(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    @classmethod
    def create_jwt_token(cls, user_id: int) -> str:
        """Создает и возвращает jwt токен с передаваемым id"""
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=JWT_EXPIRATION_TIME)
            }
        return jwt.encode(payload, cls._secret_key, algorithm=JWT_ALGORITHM)