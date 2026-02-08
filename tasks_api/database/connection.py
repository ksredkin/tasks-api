from sqlalchemy import MetaData, create_engine, Engine
from tasks_api.utils.env_config import EnvConfig
from tasks_api.database.models import metadata, users, tasks

class Database:
    def __init__(self):
        self.engine: Engine | None = None
        self.metadata: MetaData = metadata
        self.tables: dict = {'users': users, 'tasks': tasks}
    
    def _init_engine(self):
        if self.engine is None:
            config = EnvConfig()
            self.engine = create_engine(
                f"postgresql+psycopg2://{config.get_db_user()}:{config.get_db_password()}@{config.get_db_host()}:{config.get_db_port()}/{config.get_db_name()}",
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600,
                pool_pre_ping=True,
                pool_timeout=5
                )
        
        return self.engine
    
    def get_engine(self):
        return self._init_engine()
    
    def get_table(self, name: str):
        """Получает таблицу по имени"""
        return self.tables[name]
    
    def reset(self):
        """Закрыть подключения"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
    
    def reconnect(self):
        """Переподключиться"""
        self.reset()
        self._init_engine()

db = Database()

engine = db.get_engine()
tasks = db.get_table("tasks")
users = db.get_table("users")