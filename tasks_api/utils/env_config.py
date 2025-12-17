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

        if not self.secret_key:
            raise ValueError("SECRET_KEY не установлен в .env файле")
        
    def get_secret_key(self) -> str:
        return self.secret_key