from sqlalchemy import Column, String, Integer, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    text = Column(Text)
    state = Column(String)
    date = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    user = relationship("User", back_populates="tasks")