from tasks_api.database.orm_models import Task, User
from tasks_api.database.connection import db
from tasks_api.utils.logger import Logger
from datetime import datetime, timezone, timedelta
from tasks_api.utils.helpers import get_next_run_datetime

logger = Logger(__name__).get_logger()

class OrmTaskRepository:
    @staticmethod
    def create_task(user_id: int, name: str, text: str, state: str, folder_id: int, recurrence_type: str = None, recurrence_day_of_week: int = None, recurrence_month_day: int = None, due_date: datetime = None, visible_from: datetime = None) -> Task | None:
        session = db.get_session()
        try:
            task = Task(user_id=user_id, name=name, text=text, state=state, folder_id=folder_id, recurrence_type=recurrence_type, recurrence_day_of_week=recurrence_day_of_week, recurrence_month_day=recurrence_month_day, next_run=get_next_run_datetime(recurrence_type, recurrence_day_of_week, recurrence_month_day), due_date=due_date, visible_from=visible_from)
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
    def get_tasks_stats(user_id: int) -> dict | None:
        session = db.get_session()
        try:
            total = session.query(Task).filter(Task.user_id == user_id).count()
            done = session.query(Task).filter(Task.user_id == user_id, Task.state == "Done").count()
            active = session.query(Task).filter(Task.user_id == user_id, Task.state == "Active").count()            
            completion_rate = round((done / total * 100) if total > 0 else 0.0, 2)

            return {"total": total, "done": done, "active": active, "completion_rate": completion_rate}
        except Exception as e:
            logger.warning(f"Ошибка получения статистики задач: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_tasks_today(user_id: int) -> list[Task] | None:
        session = db.get_session()
        try:
            tasks = session.query(Task).filter(Task.visible_from <= datetime.now(timezone.utc), Task.user_id == user_id).all()
            return tasks
        except Exception as e:
            logger.warning(f"Ошибка получения задач на сегодня: {e}")
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
    def update_task(user_id: int, task_id: int, name: str, text: str, state: str, folder_id: int, recurrence_type: str = None, recurrence_day_of_week: int = None, recurrence_month_day: int = None, due_date: datetime = None, visible_from: datetime = None) -> Task | None:
        session = db.get_session()
        try:
            task = session.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()

            if not task:
                return None

            task.name = name
            task.text = text
            task.state = state
            task.date = datetime.now(timezone.utc)
            task.folder_id = folder_id
            task.recurrence_type = recurrence_type
            task.recurrence_day_of_week = recurrence_day_of_week
            task.recurrence_month_day = recurrence_month_day, 
            task.next_run = get_next_run_datetime(recurrence_type, recurrence_day_of_week, recurrence_month_day)
            task.due_date = due_date
            task.visible_from = visible_from

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

    @staticmethod
    def get_user_tasks_in_folder(user_id: int, folder_id: int) -> list[dict] | None:
        session = db.get_session()
        try:
            return session.query(Task).filter(Task.user_id == user_id, Task.folder_id == folder_id).all()
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось получить папки пользователя: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_repeat_tasks() -> bool:
        session = db.get_session()
        try:
            tasks = session.query(Task).filter(Task.state == "Done", Task.next_run <= datetime.now(timezone.utc)).all()

            if not tasks:
                return False

            for task in tasks:
                task.state = "Active"
                next_creating = get_next_run_datetime(task.recurrence_type, task.recurrence_day_of_week, task.recurrence_month_day)
                task.next_run = next_creating
                task.due_date = next_creating

            session.commit()

            for task in tasks:
                session.refresh(task)

            return True
        except Exception as e:
            session.rollback()
            logger.warning(f"Ошибка при попытке обновить повторяющиеся задачи: {e}")
            return False
        finally:
            session.close()