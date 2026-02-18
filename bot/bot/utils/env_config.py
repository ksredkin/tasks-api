from dotenv import load_dotenv
import os

class EnvConfig():
    """Singleton: загружает и хранит переменные из .env"""
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        load_dotenv()

        self.token = os.getenv("TOKEN")

        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME", "bot_db")

        self.api_host = os.getenv("API_HOST")
        self.api_port = os.getenv("API_PORT", 8000)

        if not self.token:
            raise ValueError("TOKEN бота не установлен в .env файле")
        
        if not self.db_password:
            raise ValueError("DB_PASSWORD не установлен в .env файле")
        if not self.db_host:
            raise ValueError("DB_HOST не установлен в .env файле")
        if not self.db_port:
            raise ValueError("DB_PORT не установлен в .env файле")
        
        if not self.api_host:
            raise ValueError("API_HOST не установлен в .env файле")

    def get_token(self) -> str:
        return self.token
    
    def get_db_user(self) -> str:
        return self.db_user
    
    def get_db_password(self) -> str:
        return self.db_password
    
    def get_db_host(self) -> str:
        return self.db_host
    
    def get_db_port(self) -> str:
        return self.db_port
    
    def get_db_name(self) -> str:
        return self.db_name
    
    def get_api_port(self) -> str:
        return self.api_port 
    
    def get_api_host(self) -> str:
        return self.api_host 