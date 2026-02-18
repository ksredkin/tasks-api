from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column, BigInteger

Base = DeclarativeBase()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)