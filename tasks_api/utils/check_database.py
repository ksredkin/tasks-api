from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger
import sqlite3
import os

logger = Logger(__name__).get_logger()

def check_database(force_recreate: bool = False):
    """Проверяет наличие базы данных, при отсутствии создает"""
    env_config = EnvConfig()
    DATABASE_PATH = env_config.get_database_path()
    DATABASE_SCRIPT_PATH = env_config.get_database_script_path()

    try:
        logger.info("Проверка наличия базы данных")

        if force_recreate and os.path.exists(DATABASE_PATH):
            logger.info("Принудительное пересоздание базы данных")
            os.unlink(DATABASE_PATH)

        if os.path.exists(DATABASE_PATH) and not force_recreate:
            logger.info("База данных уже существует")
            return

        if not force_recreate:
            logger.info("База данных не найдена: создание новой")

        with open(DATABASE_SCRIPT_PATH, "r") as f:
            script = f.read()

        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.executescript(script)

        logger.info("База данных успешно создана")
    
    except Exception as e:
        logger.critical(f"Ошибка при проверке наличия или создании базы данных: {e}")
        raise