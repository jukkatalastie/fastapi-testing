"""add content column to posts table

Revision ID: 14f63d07807d
Revises: 11c1831b3f8f
Create Date: 2024-08-10 16:33:32.584166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14f63d07807d'
down_revision: Union[str, None] = '11c1831b3f8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')
