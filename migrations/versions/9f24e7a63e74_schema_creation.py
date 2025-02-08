"""schema creation

Revision ID: 9f24e7a63e74
Revises: 
Create Date: 2025-02-08 06:17:22.327152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f24e7a63e74'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        create schema if not exists ai_coder_agent;
        """
    ))

def downgrade() -> None:
    pass
