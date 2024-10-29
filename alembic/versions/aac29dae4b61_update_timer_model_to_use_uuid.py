"""Update Timer model to use UUID

Revision ID: aac29dae4b61
Revises: 
Create Date: 2024-10-07 13:52:54.399921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = 'aac29dae4b61'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(conn, table_name, column_name):
    """Check if a column exists in a given table."""
    inspector = reflection.Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    # Get the connection object
    conn = op.get_bind()

    # Check if the 'timers' table already exists
    if not conn.dialect.has_table(conn, 'timers'):
        op.create_table('timers',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('url', sa.String(), nullable=False),
            sa.Column('hours', sa.Integer(), nullable=False),
            sa.Column('minutes', sa.Integer(), nullable=False),
            sa.Column('seconds', sa.Integer(), nullable=False),
            sa.Column('expiration_time', sa.Float(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # If the table already exists, add the new column if it doesn't exist
        if not column_exists(conn, 'timers', 'expiration_time'):
            op.add_column('timers', sa.Column('expiration_time', sa.Float(), nullable=True))


def downgrade() -> None:
    # Drop the table if it exists
    op.drop_table('timers')
