"""second try

Revision ID: faf724fc6225
Revises: be73c44fe690
Create Date: 2025-06-19 16:18:19.636953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faf724fc6225'
down_revision: Union[str, Sequence[str], None] = 'be73c44fe690'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('table_name', 'location_id',
        existing_type=sa.String(length=50),
        type_=sa.Integer(),
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
