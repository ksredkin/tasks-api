from tasks_api.core.config import JWT_EXPIRATION_TIME, JWT_ALGORITHM
from tasks_api.utils.response_factory import ResponseFactory
from datetime import datetime, timezone, timedelta
from fastapi import status
from jose import jwt, JWTError

class JWTManager:
    """Класс для работы с jwt"""
    _secret_key = None

    @classmethod
    def set_secret_key(cls, secret_key: str):
        if cls._secret_key is None:
            cls._secret_key = secret_key

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """Извлекает payload токена"""
        try:
            payload = jwt.decode(token, cls._secret_key, algorithms=JWT_ALGORITHM)
            return payload

        except JWTError as e:
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