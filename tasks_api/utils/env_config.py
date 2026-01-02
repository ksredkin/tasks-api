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
        self.database_path = os.getenv("DATABASE_PATH", "tasks_api/repositories/database.db")
        self.database_script_path = os.getenv("DATABASE_SCRIPT_PATH", "tasks_api/repositories/database.sql")

        if not self.secret_key:
            raise ValueError("SECRET_KEY не установлен в .env файле")
        
    def get_secret_key(self) -> str:
        return self.secret_key
    
    def get_database_path(self):
        return self.database_path
    
    def get_database_script_path(self):
        return self.database_script_path