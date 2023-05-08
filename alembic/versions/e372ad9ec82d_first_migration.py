"""first migration

Revision ID: e372ad9ec82d
Revises: 
Create Date: 2023-05-08 13:08:45.901105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e372ad9ec82d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("start_date", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("projects")
