"""Created project_users assignment table

Revision ID: f43a0ba0764b
Revises: be8b3e2fd4a8
Create Date: 2023-06-04 10:26:50.674306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f43a0ba0764b'
down_revision = 'be8b3e2fd4a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
       'project_user',
       sa.Column('id', sa.Integer(), primary_key=True),
       sa.Column('project_id', sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
       sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        )



def downgrade() -> None:
    op.drop_table('project_users')
