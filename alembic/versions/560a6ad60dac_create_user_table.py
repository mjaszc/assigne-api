"""Create user table

Revision ID: 560a6ad60dac
Revises: 
Create Date: 2023-05-25 21:37:57.359024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560a6ad60dac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("password", sa.String(128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
