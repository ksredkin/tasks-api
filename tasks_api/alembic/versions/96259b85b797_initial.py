"""Initial

Revision ID: 96259b85b797
Revises: 
Create Date: 2026-02-07 18:17:30.748768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '96259b85b797'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('login', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True)
    )
    
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('date', sa.TIMESTAMP(timezone=True), default=sa.func.timezone('UTC', sa.func.current_timestamp()))
    )

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')