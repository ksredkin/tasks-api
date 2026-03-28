from tasks_api.utils.logger import Logger
import psycopg2
from sqlalchemy import create_engine
import os
import subprocess

logger = Logger(__name__).get_logger()

def check_database():
    try:
        logger.info("Проверка PostgreSQL...")
        db_name = os.getenv("DB_NAME")

        try:
            engine = create_engine(f"postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}")

            with engine.connect() as _:
                logger.info(f"База данных {db_name} существует")

            engine.dispose()
        
        except Exception:
            logger.info(f"База {db_name} не найдена, создаём...")
            
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database="postgres",
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            conn.autocommit = True
            
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            
            cursor.close()
            conn.close()
            logger.info(f"База {db_name} создана")

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=db_name,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
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
        logger.info("PostgreSQL готов к работе")
    
    except Exception as e:
        logger.critical(f"Ошибка: {e}")
        raise