"""created logs table

Revision ID: b9655bcbc826
Revises: 9ae48aa75225
Create Date: 2023-07-20 13:21:54.496510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime


# revision identifiers, used by Alembic.
revision = 'b9655bcbc826'
down_revision = '9ae48aa75225'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'logs',
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("timestamp", DateTime, server_default=sa.func.now()),
        sa.Column("action", sa.String(), index=True),
        sa.Column("details", sa.String())
    )


def downgrade() -> None:
    pass
