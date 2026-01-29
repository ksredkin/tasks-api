from tasks_api.core.config import DATABASE_SCRIPT_PATH
from dotenv import load_dotenv
import os

class EnvConfig:
    """Singleton: загружает и хранит переменные из .env"""
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        load_dotenv()

        self.secret_key = os.getenv("SECRET_KEY")
        self.database_script_path = os.getenv("DATABASE_SCRIPT_PATH", DATABASE_SCRIPT_PATH)

        self.check_database_env_vars()

        if not self.secret_key:
            raise ValueError("SECRET_KEY не установлен в .env файле")
        
    def get_db_host(self):
        return os.getenv("DB_HOST", "localhost")
    
    def get_db_port(self):
        return int(os.getenv("DB_PORT", 5432))
    
    def get_db_name(self):
        return os.getenv("DB_NAME", "tasks_db")
    
    def get_db_user(self):
        return os.getenv("DB_USER", "postgres")
    
    def get_db_password(self):
        return os.getenv("DB_PASSWORD", "")

    def check_database_env_vars(self):
        required_vars = [
            'DB_HOST',
            'DB_PORT', 
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Отсутствуют переменные окружения: {missing}")

    def get_secret_key(self) -> str:
        return self.secret_key
    
    def get_database_script_path(self):
        return self.database_script_path