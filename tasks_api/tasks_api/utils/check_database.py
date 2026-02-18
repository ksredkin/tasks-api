from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger
import psycopg2
from sqlalchemy import create_engine

logger = Logger(__name__).get_logger()

def check_database():
    try:
        logger.info("Проверка PostgreSQL...")
        config = EnvConfig()
        db_name = config.get_db_name()

        try:
            engine = create_engine(f"postgresql+psycopg2://{config.get_db_user()}:{config.get_db_password()}@{config.get_db_host()}:{config.get_db_port()}/{db_name}")

            with engine.connect() as _:
                logger.info(f"База данных {db_name} существует")

            engine.dispose()
        
        except Exception:
            logger.info(f"База {db_name} не найдена, создаём...")
            
            conn = psycopg2.connect(
                host=config.get_db_host(),
                port=config.get_db_port(),
                database="postgres",
                user=config.get_db_user(),
                password=config.get_db_password()
            )
            conn.autocommit = True
            
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            
            cursor.close()
            conn.close()
            logger.info(f"База {db_name} создана")

        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database=db_name,
            user=config.get_db_user(),
            password=config.get_db_password()
        )
        conn.autocommit = False
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users LIMIT 0")
            logger.info("Таблица users существует")
        except psycopg2.errors.UndefinedTable:
            logger.info("Таблиц нет, создаём...")
            
            conn.rollback()

            logger.info("Применяем миграции Alembic...")
            import subprocess

            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logger.error(f"Ошибка миграций: {result.stderr}")
                raise Exception("Миграции не применены")

            logger.info("Миграции успешно применены")
            logger.info("Таблицы созданы")
        
        cursor.close()
        conn.close()
        
        from tasks_api.database.connection import db
        db.reconnect()

        logger.info("PostgreSQL готов к работе")
    
    except Exception as e:
        logger.critical(f"Ошибка: {e}")
        raise