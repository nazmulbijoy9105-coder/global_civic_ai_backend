"""initial tables

Revision ID: 2c02694afb2e
Revises: 98ec6d6d4066
Create Date: 2026-02-13 21:56:50.572049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c02694afb2e'
down_revision: Union[str, Sequence[str], None] = '98ec6d6d4066'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
