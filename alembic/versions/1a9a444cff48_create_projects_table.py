"""Create projects table

Revision ID: 1a9a444cff48
Revises: 560a6ad60dac
Create Date: 2023-05-25 21:38:22.245680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a9a444cff48'
down_revision = '560a6ad60dac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("projects")
