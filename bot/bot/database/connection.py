from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from bot.utils.env_config import EnvConfig

config = EnvConfig()

engine = create_async_engine(f"postgresql+asyncpg://{config.get_db_user()}:{config.get_db_password()}@{config.get_db_host()}:{config.get_db_port()}/{config.get_db_name()}")

create_session = sessionmaker(bind=engine, expire_on_commit=False) 