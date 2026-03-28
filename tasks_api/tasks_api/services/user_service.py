from tasks_api.repositories.orm_user_repository import OrmUserRepository
from tasks_api.database.orm_models import User
from tasks_api.utils.jwt import JWTManager
from passlib.context import CryptContext

context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class UserService:
    """Сервис для работы с пользователями"""
    async def create_new_user(login: str, password: str) -> User|None:
        """Создает нового пользователя, возвращает успех или нет в bool"""
        password = await OrmUserRepository.get_user_password_by_login(login)
        if password:
            return None
        user = await OrmUserRepository.create_user(login, context.hash(password))
        return user
    
    async def login(login: str, password: str) -> str|None:
        """При верных логине и пароле возвращает jwt токен, при неверных - None"""
        user = await OrmUserRepository.get_user_by_login(login)
        if not user:
            return None
        if not context.verify(password, user.password):
            return None
        token = JWTManager.create_jwt_token(user.id)
        return token