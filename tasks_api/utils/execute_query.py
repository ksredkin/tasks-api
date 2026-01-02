from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger
import sqlite3

logger = Logger(__name__).get_logger()

def execute_query(query: str, params: tuple = ()):
    """Выполняет запрос к базе данных"""
    config = EnvConfig()
    
    try:
        logger.info(f"Выполнение SQL запроса: {query[:100]}" + ("..." if len(query) > 100 else ""))
        
        with sqlite3.connect(config.get_database_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if query.upper().startswith("SELECT") or "RETURNING" in query.upper():
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            
            conn.commit()
            logger.info(f"Результат выполнения SQL запроса: {result}")
            return result
    
    except Exception as e:
        logger.critical(f"Не удалось выполнить SQL запрос: {e}")
        raise