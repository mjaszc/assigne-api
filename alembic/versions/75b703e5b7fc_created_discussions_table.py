"""created discussions table

Revision ID: 75b703e5b7fc
Revises: b421dc5e9c37
Create Date: 2023-07-17 15:18:29.790874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b703e5b7fc'
down_revision = 'b421dc5e9c37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'discussions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('discussions')
