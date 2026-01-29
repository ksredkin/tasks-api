from tasks_api.repositories.user_repository import UserRepository
from tasks_api.utils.jwt import JWTManager
from passlib.context import CryptContext

context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class UserService:
    """Сервис для работы с пользователями"""
    def create_new_user(login: str, password: str) -> bool:
        """Создает нового пользователя, возвращает успех или нет в bool"""
        if UserRepository.get_user_password(login):
            return False
        UserRepository.create_user(login, context.hash(password))
        return True
    
    def login(login: str, password: str) -> str | None:
        """При верных логине и пароле возвращает jwt токен, при неверных - None"""
        if not context.verify(password, UserRepository.get_user_password(login)):
            return None
        user_id = UserRepository.get_user_id(login)
        token = JWTManager.create_jwt_token(user_id)
        return token