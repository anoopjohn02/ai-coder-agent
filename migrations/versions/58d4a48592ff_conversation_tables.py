"""conversation tables

Revision ID: 58d4a48592ff
Revises: 9f24e7a63e74
Create Date: 2025-02-08 06:17:59.863610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58d4a48592ff'
down_revision: Union[str, None] = '9f24e7a63e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        CREATE TABLE ai_coder_agent.conversation_history (
            id uuid PRIMARY KEY,
            retriever varchar NULL,
            memory varchar NULL,
            llm varchar NULL,
            created_on timestamp NOT NULL,
            user_id uuid NOT NULL,
            deleted boolean default false
        );
        """
    ))


def downgrade() -> None:
    op.execute(sa.DDL(
        """
        DROP TABLE ai_coder_agent.conversation_history;
        """
    ))
