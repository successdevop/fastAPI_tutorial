"""add cancelled status

Revision ID: 6e815a4fc834
Revises: dcc1e32f823f
Create Date: 2026-06-19 19:56:42.276913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e815a4fc834'
down_revision: Union[str, Sequence[str], None] = 'dcc1e32f823f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TYPE shipmentstatus ADD VALUE IF NOT EXISTS 'CANCELLED';"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
