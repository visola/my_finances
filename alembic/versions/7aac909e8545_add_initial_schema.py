"""Add initial schema

Revision ID: 7aac909e8545
Revises: 003edcc5484d
Create Date: 2021-01-13 23:20:10.603537

"""
from alembic import op
from sqlalchemy import Column, Date, Integer, Numeric, String


# revision identifiers, used by Alembic.
revision = '7aac909e8545'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        Column('id', Integer, nullable=False, primary_key=True),
        Column('description', String(150)),
        Column('user_id', Integer, nullable=False),
        Column('category_id', Integer),
        Column('date', Date, nullable=False),
        Column('value', Numeric, nullable=False),
        Column('source_accnt_id', Integer, nullable=False),
        Column('link_id', String(150)),
    )

    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('email', String(100), nullable=False),
        Column('password', String(150), nullable=False),
    )

    op.create_table(
        'categories',
        Column('id', Integer, nullable=False, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('user_id', Integer, nullable=False),
    )

    op.create_table(
        'accounts',
        Column('id', Integer, nullable=False, primary_key=True),
        Column('name', String(100)),
        Column('user_id', Integer, nullable=False),
        Column('type', String(100)),
    )

    op.create_table(
        'preferences',
        Column('user_id', Integer, nullable=False, primary_key=True),
        Column('preference', String(60), nullable=False),
    )

def downgrade():
    pass
