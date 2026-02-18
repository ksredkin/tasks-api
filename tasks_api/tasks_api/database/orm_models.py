from sqlalchemy import Column, String, Integer, TIMESTAMP, Text, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")
    folders = relationship("Folder", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    text = Column(Text)
    state = Column(String)
    date = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    user = relationship("User", back_populates="tasks")
    folder = relationship("Folder", back_populates="tasks")

class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    show_progress = Column(Boolean, nullable=False, default=False)
    user = relationship("User", back_populates="folders")
    tasks = relationship("Task", back_populates="folder")