from tasks_api.core.config import DATABASE_PATH, DATABASE_SCRIPT_PATH
from tasks_api.utils.logger import Logger
import sqlite3
import os

logger = Logger(__name__).get_logger()

def check_database():
    """Проверяет наличие базы данных, при отсутствии создает"""
    try:
        logger.info("Проверка наличия базы данных")
        if os.path.exists(DATABASE_PATH):
            logger.info("База данных уже существует")
            return

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