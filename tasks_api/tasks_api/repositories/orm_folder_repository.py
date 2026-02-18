from tasks_api.database.orm_models import Folder, User
from tasks_api.database.connection import db
from tasks_api.utils.logger import Logger

logger = Logger(__name__).get_logger()

class OrmFolderRepository:
    @staticmethod
    def create_folder(user_id: int, name: str, parent_id: int | None = None, show_progress: bool = False) -> Folder | None:
        session = db.get_session()
        try:
            folder = Folder(user_id=user_id, name=name, parent_id=parent_id, show_progress=show_progress)
            session.add(folder)
            session.commit()
            session.refresh(folder)
            return folder
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось создать папку: {e}")
            return None
        finally:
            session.close()
        
    @staticmethod
    def update_folder(user_id: int, folder_id: int, name: str, parent_id: int | None = None, show_progress: bool = False) -> Folder | None:
        session = db.get_session()
        try:
            folder = session.query(Folder).filter(Folder.id == folder_id, Folder.user_id == user_id).first()

            folder.name = name
            folder.parent_id = parent_id
            folder.show_progress = show_progress

            session.commit()
            session.refresh(folder)
            return folder
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось создать папку: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def delete_folder(user_id: int, folder_id: int) -> Folder | None:
        session = db.get_session()
        try:
            folder = session.query(Folder).filter(Folder.id == folder_id, Folder.user_id == user_id).first()
            if not folder:
                return None
            session.delete(folder)
            session.commit()
            return folder
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось создать папку: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_folders(user_id: int) -> list[Folder] | None:
        session = db.get_session()
        try:
            folders = session.get(User, user_id).folders
            return folders
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось получить папки пользователя: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_folder(user_id: int, folder_id: int) -> Folder | None:
        session = db.get_session()
        try:
            return session.query(Folder).filter(Folder.id == folder_id, Folder.user_id == user_id).first()
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось получить папки пользователя: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_user_folders_in_folder(user_id: int, folder_id: int) -> list[dict] | None:
        session = db.get_session()
        try:
            return session.query(Folder).filter(Folder.user_id == user_id, Folder.parent_id == folder_id).all()
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось получить папки пользователя: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_folder_progress(user_id: int, folder_id: int) -> float | None:
        session = db.get_session()
        from tasks_api.database.orm_models import Task
        try:
            all_tasks = session.query(Task).filter(Task.user_id == user_id, Task.folder_id == folder_id).all()
            done_tasks = session.query(Task).filter(Task.user_id == user_id, Task.folder_id == folder_id, Task.state == "Done").all()
            return round(len(done_tasks)/len(all_tasks), 2)
        except Exception as e:
            session.rollback()
            logger.warning(f"Не удалось получить папки пользователя: {e}")
            return None
        finally:
            session.close()