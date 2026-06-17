"""sync database state

Revision ID: 1a9ae97fc4fa
Revises: 5e6cfe551506
Create Date: 2026-06-17 10:09:09.063521

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a9ae97fc4fa'
down_revision: Union[str, Sequence[str], None] = '5e6cfe551506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
