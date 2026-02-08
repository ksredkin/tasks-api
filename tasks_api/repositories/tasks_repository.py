from tasks_api.database.connection import db
from sqlalchemy import select, insert, update, delete, func

class TasksRepository:
    @staticmethod
    def get_user_tasks(id: int) -> list | None:
        tasks = db.get_table("tasks")
        engine = db.get_engine()
        query = select(tasks.c.id, tasks.c.name, tasks.c.text, tasks.c.state, tasks.c.date).where(tasks.c.user_id == id)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        return data if data else None

    @staticmethod
    def get_user_task(task_id: int, user_id: int) -> list | None:
        tasks = db.get_table("tasks")
        engine = db.get_engine()
        query = select(tasks.c.name, tasks.c.text, tasks.c.state, tasks.c.date).where(tasks.c.user_id == user_id, tasks.c.id == task_id)
        with engine.connect() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        return data if data else None
    
    @staticmethod
    def create_task(user_id: int, name: str, text: str, state: str) -> tuple | None:
        tasks = db.get_table("tasks")
        engine = db.get_engine()
        query = insert(tasks).values(user_id=user_id, name=name, text=text, state=state, date=func.timezone('UTC', func.current_timestamp())).returning(tasks.c.id, tasks.c.date)
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            data = result.fetchall()
        return (data[0][0], data[0][1]) if data else None
    
    @staticmethod
    def update_task(user_id: int, task_id: int, name: str, text: str, state: str) -> str | None:
        tasks = db.get_table("tasks")
        engine = db.get_engine()
        query = update(tasks).values(user_id=user_id, name=name, text=text, state=state, date=func.timezone('UTC', func.current_timestamp())).where(tasks.c.user_id == user_id, tasks.c.id == task_id).returning(tasks.c.date)
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            data = result.fetchall()
        return data[0][0] if data else None
    
    @staticmethod
    def delete_task(user_id: int, task_id: int) -> list | None:
        tasks = db.get_table("tasks")
        engine = db.get_engine()
        query = delete(tasks).where(tasks.c.user_id == user_id, tasks.c.id == task_id).returning(tasks.c.name, tasks.c.text, tasks.c.state, tasks.c.date)
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            data = result.fetchall()
        return data[0] if data else None