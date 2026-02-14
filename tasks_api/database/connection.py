from sqlalchemy import create_engine, Engine
from tasks_api.utils.env_config import EnvConfig
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        self.engine: Engine | None = None
        self._SessionLocal = None
    
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
    
    def get_session(self):
        """Возвращает новую сессию"""
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        return self._SessionLocal()
    
    def get_engine(self):
        return self._init_engine()
    
    def reset(self):
        """Закрыть подключения"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self._SessionLocal = None
    
    def reconnect(self):
        """Переподключиться"""
        self.reset()
        self._init_engine()

db = Database()
engine = db.get_engine()