from sqlalchemy import MetaData, Table, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
)

tasks = Table(
    'tasks',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('name', String, nullable=False),
    Column('text', Text),
    Column('state', String, default='active'),
    Column('date', TIMESTAMP(timezone=True), server_default=func.now()),
)