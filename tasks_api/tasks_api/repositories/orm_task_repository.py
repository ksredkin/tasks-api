from tasks_api.database.orm_models import Task
from tasks_api.database.connection import session
from tasks_api.utils.logger import Logger
from datetime import datetime, timezone
from tasks_api.utils.helpers import get_next_run_datetime
from sqlalchemy import select, func

logger = Logger(__name__).get_logger()

class OrmTaskRepository:
    @staticmethod
    async def create_task(user_id: int, name: str, text: str, state: str, folder_id: int, recurrence_type: str = None, recurrence_day_of_week: int = None, recurrence_month_day: int = None, due_date: datetime = None, visible_from: datetime = None) -> Task|None:
        async with session() as conn:
            try:
                task = Task(user_id=user_id, name=name, text=text, state=state, folder_id=folder_id, recurrence_type=recurrence_type, recurrence_day_of_week=recurrence_day_of_week, recurrence_month_day=recurrence_month_day, next_run=get_next_run_datetime(recurrence_type, recurrence_day_of_week, recurrence_month_day), due_date=due_date, visible_from=visible_from)
                conn.add(task)
                await conn.commit()
                await conn.refresh(task)
                return task
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка создания задачи: {e}")
                return None

    @staticmethod
    async def import_tasks(user_id: int, tasks: list[Task], import_type: str) -> bool:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id))
                user_tasks = result.scalars().all()

                if not user_tasks:
                    return False
                
                if any(task.id is None for task in tasks):
                    return False

                match import_type:
                    case "delete":
                        for task in user_tasks:
                            await conn.delete(task)

                        for task_data in tasks:
                            new_task = Task(user_id=user_id, name=task_data.name, text=task_data.text, state=task_data.state, folder_id=task_data.folder_id, recurrence_type=task_data.recurrence_type, recurrence_day_of_week=task_data.recurrence_day_of_week, recurrence_month_day=task_data.recurrence_month_day, next_run=task_data.next_run, due_date=task_data.due_date, visible_from=task_data.visible_from)
                            conn.add(new_task)

                    case "create":
                        for task_data in tasks:
                            new_task = Task(user_id=user_id, name=task_data.name, text=task_data.text, state=task_data.state, folder_id=task_data.folder_id, recurrence_type=task_data.recurrence_type, recurrence_day_of_week=task_data.recurrence_day_of_week, recurrence_month_day=task_data.recurrence_month_day, next_run=task_data.next_run, due_date=task_data.due_date, visible_from=task_data.visible_from)
                            conn.add(new_task)

                    case "update":
                        existing_tasks = {t.id: t for t in user_tasks}
                        for task_data in tasks:
                            if task_data.id in existing_tasks:
                                existing = existing_tasks[task_data.id]
                                existing.text = task_data.text
                                existing.state = task_data.state
                                existing.folder_id = task_data.folder_id
                                existing.recurrence_type = task_data.recurrence_type
                                existing.recurrence_day_of_week = task_data.recurrence_day_of_week
                                existing.recurrence_month_day = task_data.recurrence_month_day
                                existing.next_run = task_data.next_run
                                existing.due_date = task_data.due_date
                                existing.visible_from = task_data.visible_from
                            else:
                                new_task = Task(user_id=user_id, name=task_data.name, text=task_data.text, state=task_data.state, folder_id=task_data.folder_id, recurrence_type=task_data.recurrence_type, recurrence_day_of_week=task_data.recurrence_day_of_week, recurrence_month_day=task_data.recurrence_month_day, next_run=task_data.next_run, due_date=task_data.due_date, visible_from=task_data.visible_from)
                                conn.add(new_task)
                                
                    case _:
                        return False

                await conn.commit()
                return True
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка импорта задач: {e}")
                return False

    @staticmethod
    async def get_user_tasks(user_id: int) -> list[Task]|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id))
                return result.scalars().all()
            except Exception as e:
                logger.warning(f"Ошибка получения задач: {e}")
                return None

    @staticmethod
    async def get_tasks_stats(user_id: int) -> dict|None:
        async with session() as conn:
            try:
                result1 = await conn.execute(select(func.count()).where(Task.user_id == user_id))
                total = result1.scalar() or 0

                result2 = await conn.execute(select(func.count()).where(Task.user_id == user_id, Task.state == "Done"))
                done = result2.scalar() or 0
                
                result3 = await conn.execute(select(func.count()).where(Task.user_id == user_id, Task.state == "Active"))            
                active = result3.scalar() or 0
                
                completion_rate = round((done / total * 100) if total > 0 else 0.0)

                return {"total": total, "done": done, "active": active, "completion_rate": completion_rate}
            except Exception as e:
                logger.warning(f"Ошибка получения статистики задач: {e}")
                return None

    @staticmethod
    async def get_user_tasks_today(user_id: int) -> list[Task]|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.visible_from <= datetime.now(timezone.utc), Task.user_id == user_id))
                return result.scalars().all()
            except Exception as e:
                logger.warning(f"Ошибка получения задач на сегодня: {e}")
                return None

    @staticmethod
    async def get_user_task_by_id(user_id: int, task_id: int) -> Task|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id))
                return result.scalars().first()
            except Exception as e:
                logger.warning(f"Ошибка получения задачи по user_id {user_id} и id задачи {task_id}: {e}")
                return None

    @staticmethod
    async def update_task(user_id: int, task_id: int, name: str, text: str, state: str, folder_id: int, recurrence_type: str = None, recurrence_day_of_week: int = None, recurrence_month_day: int = None, due_date: datetime = None, visible_from: datetime = None) -> Task|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id))
                task = result.scalars().first()

                if not task:
                    return None

                task.name = name
                task.text = text
                task.state = state
                task.folder_id = folder_id
                task.recurrence_type = recurrence_type
                task.recurrence_day_of_week = recurrence_day_of_week
                task.recurrence_month_day = recurrence_month_day
                task.next_run = get_next_run_datetime(recurrence_type, recurrence_day_of_week, recurrence_month_day)
                task.due_date = due_date
                task.visible_from = visible_from

                await conn.commit()
                await conn.refresh(task)
                return task
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка при попытке обновить задачу: {e}")
                return None

    @staticmethod
    async def delete_task(user_id: int, task_id: int) -> Task|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id))
                task = result.scalars().first()
                if not task:
                    return None
                await conn.delete(task)
                await conn.commit()
                return task
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка при попытке удалить задачу: {e}")
                return None

    @staticmethod
    async def get_user_tasks_in_folder(user_id: int, folder_id: int) -> list[Task]|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.user_id == user_id, Task.folder_id == folder_id))
                return result.scalars().all()
            except Exception as e:
                logger.warning(f"Не удалось получить папки пользователя: {e}")
                return None

    @staticmethod
    async def update_repeat_tasks() -> bool:
        async with session() as conn:
            try:
                result = await conn.execute(select(Task).where(Task.state == "Done", Task.next_run <= datetime.now(timezone.utc)))
                tasks = result.scalars().all()

                if not tasks:
                    return False

                for task in tasks:
                    task.state = "Active"
                    next_creating = get_next_run_datetime(task.recurrence_type, task.recurrence_day_of_week, task.recurrence_month_day)
                    task.next_run = next_creating
                    task.due_date = next_creating

                await conn.commit()

                for task in tasks:
                    await conn.refresh(task)

                return True
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка при попытке обновить повторяющиеся задачи: {e}")
                return False