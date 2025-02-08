"""conversation message table

Revision ID: bc9039cbf541
Revises: 58d4a48592ff
Create Date: 2025-02-08 06:19:12.453607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc9039cbf541'
down_revision: Union[str, None] = '58d4a48592ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        CREATE TABLE ai_coder_agent.conversation_messages (
            id uuid PRIMARY KEY,
            conversation_id uuid NOT NULL,
            "role" varchar NOT NULL,
            "content" text NOT NULL,
            created_on timestamp NOT NULL,
            CONSTRAINT conversation_messages_fk FOREIGN KEY (conversation_id) REFERENCES ai_coder_agent.conversation_history(id) ON DELETE CASCADE
        );
        """
    ))


def downgrade() -> None:
    op.execute(sa.DDL(
        """
        DROP TABLE ai_coder_agent.conversation_messages;
        """
    ))
