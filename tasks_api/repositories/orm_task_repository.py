from tasks_api.database.orm_models import Task, User
from tasks_api.database.connection import db
from tasks_api.utils.logger import Logger
from datetime import datetime, timezone

logger = Logger(__name__).get_logger()

class OrmTaskRepository:
    @staticmethod
    def create_task(user_id: int, name: str, text: str, state: str) -> Task | None:
        session = db.get_session()
        try:
            task = Task(user_id=user_id, name=name, text=text, state=state, date=datetime.now(timezone.utc))
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        except Exception as e:
            session.rollback()
            logger.warning(f"Ошибка создания задачи: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_user_tasks(user_id: int) -> list[Task] | None:
        session = db.get_session()
        try:
            user = session.get(User, user_id)
            tasks = user.tasks
            return tasks
        except Exception as e:
            logger.warning(f"Ошибка получения задач: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_task_by_id(user_id: int, task_id: int) -> Task | None:
        session = db.get_session()
        try:
            return session.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
        except:
            return None
        finally:
            session.close()

    @staticmethod
    def update_task(user_id: int, task_id: int, name: str, text: str, state: str) -> Task | None:
        session = db.get_session()
        try:
            task = session.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
            
            if not task:
                return None
            
            task.name = name
            task.text = text
            task.state = state
            task.date = datetime.now(timezone.utc)

            session.commit()
            session.refresh(task)
            return task
        except Exception as e:
            session.rollback()
            logger.warning(f"Ошибка при попытке обновить задачу: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def delete_task(user_id: int, task_id: int) -> Task | None:
        session = db.get_session()
        try:
            task = session.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
            if not task:
                return None
            session.delete(task)
            session.commit()
            return task
        except Exception as e:
            session.rollback()
            logger.warning(f"Ошибка при попытке удалить задачу: {e}")
            return None
        finally:
            session.close()