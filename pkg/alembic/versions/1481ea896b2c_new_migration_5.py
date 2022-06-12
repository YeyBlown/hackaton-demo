"""New Migration 5

Revision ID: 1481ea896b2c
Revises: 4a0d22503e1a
Create Date: 2022-06-12 22:36:25.322163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1481ea896b2c'
down_revision = '4a0d22503e1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(), nullable=True))
    op.drop_column('user', 'login')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
