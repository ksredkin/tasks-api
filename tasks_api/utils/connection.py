from sqlalchemy import MetaData, create_engine, Engine
from tasks_api.utils.env_config import EnvConfig

class Database:
    def __init__(self):
        self.engine: Engine | None = None
        self.metadata: MetaData | None = None
        self.tables: dict = {}
    
    def _init_engine(self):
        """Инициализирует engine при первом обращении"""
        if self.engine is None:
            config = EnvConfig()
            self.engine = create_engine(f"postgresql+psycopg2://{config.get_db_user()}:{config.get_db_password()}@{config.get_db_host()}:{config.get_db_port()}/{config.get_db_name()}")
        
        return self.engine
    
    def _init_metadata(self):
        """Инициализирует metadata при первом обращении"""
        if self.metadata is None:
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
        return self.metadata
    
    def get_engine(self):
        return self._init_engine()
    
    def get_metadata(self):
        return self._init_metadata()
    
    def get_table(self, name: str):
        """Получает таблицу по имени"""
        if name not in self.tables:
            self.tables[name] = self.metadata.tables[name]
        return self.tables[name]
    
    def reset(self):
        """Сбросить подключение"""
        if self.engine:
            self.engine.dispose()

        self.engine = None
        self.metadata = None
        self.tables.clear()

        self.engine = self._init_engine()
        self.metadata = self._init_metadata()

    def _reset(self):
        """Сбросить подключение"""
        if self.engine:
            self.engine.dispose()

        self.engine = None
        self.metadata = None
        self.tables.clear()

db = Database()

engine = db.get_engine()

metadata = db.get_metadata()
tasks = db.get_table("tasks")
users = db.get_table("users")