from tasks_api.database.orm_models import User
from tasks_api.database.connection import session
from tasks_api.utils.logger import Logger
from sqlalchemy import select

logger = Logger(__name__).get_logger()

class OrmUserRepository:
    @staticmethod
    async def create_user(login: str, password: str) -> User|None:
        async with session() as conn:
            try:
                user = User(login=login, password=password)
                conn.add(user)
                await conn.commit()
                await conn.refresh(user)
                return user
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка при создании пользователя: {e}")
                return None

    @staticmethod
    async def get_user_by_id(user_id: int) -> User|None:
        async with session() as conn:
            try:
                user = await conn.execute(select(User).where(User.id == user_id))
                return user.scalars().first()
            except Exception as e:
                logger.warning(f"Не удалось найти пользователя с id {user_id} в бд: {e}")
                return None

    @staticmethod
    async def get_user_by_login(user_login: str) -> User|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(User).where(User.login == user_login))
                user = result.scalars().first()
                return user
            except Exception as e:
                logger.warning(f"Не удалось найти пользователя с логином {user_login} в бд: {e}")
                return None

    @staticmethod
    async def get_user_id_by_login(user_login: str) -> int|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(User.id).where(User.login == user_login))
                return result.scalars()
            except Exception as e:
                logger.warning(f"Не удалось получить id пользователя по логину {user_login}: {e}")
                return None
    
    @staticmethod
    async def get_user_password_by_login(user_login: str) -> str|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(User.password).where(User.login == user_login))
                return result.scalars()
            except Exception as e:
                logger.warning(f"Не удалось получить пароль пользователя по логину {user_login}: {e}")
                return None