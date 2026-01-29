from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger
import psycopg2

logger = Logger(__name__).get_logger()

def check_database():
    env_config = EnvConfig()
    
    db_name = env_config.get_db_name()
    
    try:
        logger.info("Проверка PostgreSQL...")
        
        try:
            conn = psycopg2.connect(
                host=env_config.get_db_host(),
                port=env_config.get_db_port(),
                database=db_name,
                user=env_config.get_db_user(),
                password=env_config.get_db_password()
            )
            logger.info(f"База данных {db_name} существует")
            conn.close()
            
        except psycopg2.OperationalError:
            logger.info(f"База {db_name} не найдена, создаём...")
            
            conn = psycopg2.connect(
                host=env_config.get_db_host(),
                port=env_config.get_db_port(),
                database="postgres",
                user=env_config.get_db_user(),
                password=env_config.get_db_password()
            )
            conn.autocommit = True
            
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            
            cursor.close()
            conn.close()
            logger.info(f"База {db_name} создана")
        
        conn = psycopg2.connect(
            host=env_config.get_db_host(),
            port=env_config.get_db_port(),
            database=db_name,
            user=env_config.get_db_user(),
            password=env_config.get_db_password()
        )
        conn.autocommit = False
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users LIMIT 0")
            logger.info("Таблица users существует")
        except psycopg2.errors.UndefinedTable:
            logger.info("Таблиц нет, создаём...")
            
            conn.rollback()

            sql_file = env_config.get_database_script_path()

            with open(sql_file, 'r') as f:
                sql_script = f.read()
            
            cursor.execute(sql_script)
            conn.commit()
            logger.info("Таблицы созданы")
        
        cursor.close()
        conn.close()
        
        logger.info("PostgreSQL готов к работе")
    
    except Exception as e:
        logger.critical(f"Ошибка: {e}")
        raise