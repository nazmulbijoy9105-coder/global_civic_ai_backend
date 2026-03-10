"""add role and trait columns

Revision ID: 4fb278b2fb3a
Revises: create_questions_responses
Create Date: 2026-03-10 07:27:19.001598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fb278b2fb3a'
down_revision: Union[str, Sequence[str], None] = 'create_questions_responses'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'role' to users table with a default value
    op.add_column('users', sa.Column('role', sa.String(), nullable=True, server_default='user'))
    
    # Add 'trait' to responses table
    # Note: We allow nullable=True initially to avoid errors with existing data
    op.add_column('responses', sa.Column('trait', sa.String(), nullable=True))

def downgrade() -> None:
    # Reverse the changes if needed
    op.drop_column('responses', 'trait')
    op.drop_column('users', 'role')
