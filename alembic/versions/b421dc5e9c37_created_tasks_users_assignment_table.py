"""created tasks users assignment table

Revision ID: b421dc5e9c37
Revises: f43a0ba0764b
Create Date: 2023-06-12 17:33:31.903236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b421dc5e9c37'
down_revision = 'f43a0ba0764b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
       'task_user',
       sa.Column('id', sa.Integer(), primary_key=True),
       sa.Column('task_id', sa.Integer(), sa.ForeignKey("tasks.id"), nullable=False),
       sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        )


def downgrade() -> None:
    op.drop_table('task_user')
