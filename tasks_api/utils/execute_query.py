import psycopg2
from psycopg2.extras import RealDictCursor
from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger

logger = Logger(__name__).get_logger()

def execute_query(query: str, params: tuple = ()):
    config = EnvConfig()
    
    try:
        logger.info(f"Выполнение PostgreSQL запроса: {query[:100]}" + ("..." if len(query) > 100 else ""))
        
        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database=config.get_db_name(),
            user=config.get_db_user(),
            password=config.get_db_password()
        )
        
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        conn.commit()
        
        query_upper = query.upper().strip()
        if query_upper.startswith("SELECT") or "RETURNING" in query_upper:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        logger.info(f"Результат выполнения SQL запроса: {result}")
        return result
    
    except Exception as e:
        logger.critical(f"Не удалось выполнить SQL запрос: {e}")
        raise