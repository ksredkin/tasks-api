from tasks_api.database.orm_models import User
from tasks_api.database.connection import db
from tasks_api.utils.logger import Logger

logger = Logger(__name__).get_logger()

class OrmUserRepository:
    @staticmethod
    def create_user(login: str, password: str) -> User | None:
        session = db.get_session()
        try:
            user = User(login=login, password=password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            logger.warning(f"Ошибка при создании пользователя: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        session = db.get_session()
        try:
            return session.get(User, user_id)
        finally:
            session.close()

    @staticmethod
    def get_user_by_login(user_login: str) -> User | None:
        session = db.get_session()
        try:
            return session.query(User).filter(User.login == user_login).first()
        except Exception:
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_id_by_login(user_login: str) -> int:
        user = OrmUserRepository.get_user_by_login(user_login=user_login)
        return user.id if user else None
    
    @staticmethod
    def get_user_password_by_login(user_login: str) -> str:
        user = OrmUserRepository.get_user_by_login(user_login=user_login)
        return user.password if user else None