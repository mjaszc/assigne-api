"""Create tasks table

Revision ID: be8b3e2fd4a8
Revises: 1a9a444cff48
Create Date: 2023-05-29 16:36:46.774202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'be8b3e2fd4a8'
down_revision = '1a9a444cff48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
    )



def downgrade() -> None:
    op.drop_table('tasks')
