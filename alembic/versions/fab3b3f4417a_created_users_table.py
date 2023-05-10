"""created users table

Revision ID: fab3b3f4417a
Revises: e372ad9ec82d
Create Date: 2023-05-09 19:19:34.232467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fab3b3f4417a"
down_revision = "e372ad9ec82d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("password", sa.String(128), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
