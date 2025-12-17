from tasks_api.core.config import DATABASE_PATH
from tasks_api.utils.logger import Logger
import sqlite3

logger = Logger(__name__).get_logger()
ellipsis_if_needs = lambda x: "..." if x > 100 else ""

def execute_query(query: str, params: tuple = ()):
    """Выполняет запрос к базе данных"""
    try:
        logger.info(f"Выполнение SQL запроса: {query[:100]}" + ellipsis_if_needs(query))
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if query.upper().startswith("SELECT") or "RETURNING" in query.upper().split():
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            conn.commit()
            logger.info(f"Результат выполнения SQL запроса: {result[:100]}" + ellipsis_if_needs(result))
            return result
    except Exception as e:
        logger.critical(f"Не удалось выполнить SQL запрос: {e}")
        raise