"""Add index on user_id and created_at

Revision ID: 6726fa349235
Revises: 7d0b1f062f8f
Create Date: 2026-02-09 19:09:43.764389

"""
from typing import Sequence, Union
from alembic import op

revision: str = '6726fa349235'
down_revision: Union[str, Sequence[str], None] = '7d0b1f062f8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_index("idx_tasks_user_id_date", "tasks", ["user_id", "date"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_tasks_user_id_date", "tasks")