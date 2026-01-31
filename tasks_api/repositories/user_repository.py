from tasks_api.utils.connection import db
from sqlalchemy import select, insert

class UserRepository:
    @staticmethod
    def create_user(login: str, password: str) -> int | None:
        users = db.get_table("users")
        engine = db.get_engine()
        query = insert(users).values(login=login, password=password).returning(users.c.id)
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            data = result.fetchall()
        return data[0][0] if data else None

    @staticmethod
    def get_user_password(login: str) -> str | None:
        users = db.get_table("users")
        engine = db.get_engine()
        query = select(users.c.password).where(users.c.login == login)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        return data[0][0] if data else None
    
    @staticmethod
    def get_user_id(login: str) -> int | None:
        users = db.get_table("users")
        engine = db.get_engine()
        query = select(users.c.id).where(users.c.login == login)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        return data[0][0] if data else None
    
    @staticmethod
    def get_user_login(id: int) -> str | None:
        users = db.get_table("users")
        engine = db.get_engine()
        query = select(users.c.login).where(users.c.id == id)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        return data[0][0] if data else None