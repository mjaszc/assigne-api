"""created comments table

Revision ID: 9ae48aa75225
Revises: 75b703e5b7fc
Create Date: 2023-07-18 20:44:29.712568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae48aa75225'
down_revision = '75b703e5b7fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('discussion_comments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('discussion_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=True),
    )



def downgrade() -> None:
    op.drop_table('comments')
