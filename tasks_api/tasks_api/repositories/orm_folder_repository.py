from tasks_api.database.orm_models import Folder, Task
from tasks_api.database.connection import session
from tasks_api.utils.logger import Logger
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func

logger = Logger(__name__).get_logger()

class OrmFolderRepository:
    @staticmethod
    async def create_folder(user_id: int, name: str, parent_id: int|None = None, show_progress: bool = False) -> Folder|None:
        async with session() as conn:
            try:
                folder = Folder(user_id=user_id, name=name, parent_id=parent_id, show_progress=show_progress)
                conn.add(folder)
                await conn.commit()
                await conn.refresh(folder)
                return folder
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Не удалось создать папку: {e}")
                return None
        
    @staticmethod
    async def update_folder(user_id: int, folder_id: int, name: str, parent_id: int|None = None, show_progress: bool = False) -> Folder|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id))
                folder = result.scalars().first()

                if not folder:
                    return None

                folder.name = name
                folder.parent_id = parent_id
                folder.show_progress = show_progress

                await conn.commit()
                await conn.refresh(folder)
                return folder
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Не удалось обновить папку: {e}")
                return None

    @staticmethod
    async def delete_folder(user_id: int, folder_id: int) -> Folder|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id))
                folder = result.scalars().first()
                if not folder:
                    return None
                await conn.delete(folder)
                await conn.commit()
                return folder
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Не удалось удалить папку: {e}")
                return None

    @staticmethod
    async def get_user_folders(user_id: int) -> list[Folder]|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.user_id == user_id))
                folders = result.scalars().all()
                return folders
            except Exception as e:
                logger.warning(f"Не удалось получить папки пользователя: {e}")
                return None

    @staticmethod
    async def get_user_folder(user_id: int, folder_id: int) -> Folder|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id))
                return result.scalars().first()
            except Exception as e:
                logger.warning(f"Не удалось получить папку пользователя: {e}")
                return None

    @staticmethod
    async def get_user_folders_in_folder(user_id: int, folder_id: int) -> list[Folder]|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.user_id == user_id, Folder.parent_id == folder_id))
                return result.scalars().all()
            except Exception as e:
                logger.warning(f"Не удалось получить папки пользователя в папке: {e}")
                return None

    @staticmethod
    async def get_folder_progress(user_id: int, folder_id: int) -> float|None:
        async with session() as conn:
            try:
                result1 = await conn.execute(select(func.count()).where(Task.user_id == user_id, Task.folder_id == folder_id))
                all_tasks = result1.scalar() or 0

                result2 = await conn.execute(select(func.count()).where(Task.user_id == user_id, Task.folder_id == folder_id, Task.state == "Done"))
                done_tasks = result2.scalar() or 0

                return round(done_tasks/all_tasks * 100, 2) if all_tasks > 0 else 100.0
            except Exception as e:
                logger.warning(f"Не удалось получить прогресс папки: {e}")
                return None

    @staticmethod
    async def get_folders_stats(user_id: int) -> dict|None:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.user_id == user_id).options(joinedload(Folder.tasks)))
                folders = result.scalars().all()

                if not folders:
                    return None

                by_folder = {}
                for folder in folders:
                    tasks = folder.tasks
                    total = len(tasks)
                    done = len([task for task in tasks if task.state == "Done"])
                    active = len([task for task in tasks if task.state == "Active"])
                    completion_rate = round((done / total * 100) if total > 0 else 0.0, 2)

                    by_folder[folder.name] = {"total": total, "done": done, "active": active, "completion_rate": completion_rate}
                
                return by_folder
            except Exception as e:
                logger.warning(f"Не удалось получить статистику пользователя по папкам: {e}")
                return None

    @staticmethod
    async def import_folders(user_id: int, folders: list[Folder], import_type: str) -> bool:
        async with session() as conn:
            try:
                result = await conn.execute(select(Folder).where(Folder.user_id == user_id))
                user_folders = result.scalars().all()

                if any(folder.id is None for folder in folders):
                    return False

                match import_type:
                    case "delete":
                        for folder in user_folders:
                            await conn.delete(folder)

                        for folder_data in folders:
                            new_folder = Folder(user_id=user_id, name=folder_data.name, parent_id=folder_data.parent_id, show_progress=folder_data.show_progress)
                            conn.add(new_folder)

                    case "create":
                        for folder_data in folders:
                            new_folder = Folder(user_id=user_id, name=folder_data.name, parent_id=folder_data.parent_id, show_progress=folder_data.show_progress)
                            conn.add(new_folder)

                    case "update":
                        existing_folders = {t.id: t for t in user_folders}
                        for folder_data in folders:
                            if folder_data.id in existing_folders:
                                existing = existing_folders[folder_data.id]
                                existing.name = folder_data.name
                                existing.parent_id = folder_data.parent_id
                                existing.show_progress = folder_data.show_progress
                            else:
                                new_folder = Folder(user_id=user_id, name=folder_data.name, parent_id=folder_data.parent_id, show_progress=folder_data.show_progress)
                                conn.add(new_folder)

                    case _:
                        return False

                await conn.commit()
                return True
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Ошибка импорта папок: {e}")
                return False