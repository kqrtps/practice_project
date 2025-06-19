"""changed location_id type to integer

Revision ID: be73c44fe690
Revises: c36c4a11b25f
Create Date: 2025-06-19 16:00:28.372827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be73c44fe690'
down_revision: Union[str, Sequence[str], None] = 'c36c4a11b25f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
