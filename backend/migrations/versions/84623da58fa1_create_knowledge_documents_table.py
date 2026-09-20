"""create knowledge documents table

Revision ID: 84623da58fa1
Revises: fed6c5c996d5
Create Date: 2026-09-20 14:25:26.441279

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "84623da58fa1"
down_revision: Union[str, Sequence[str], None] = "fed6c5c996d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the knowledge_documents table."""

    op.create_table(
        "knowledge_documents",
        sa.Column(
            "id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "source",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "metadata",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "embedding",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.execute(
        """
        ALTER TABLE knowledge_documents
        ALTER COLUMN embedding TYPE vector(768)
        USING NULL::vector
        """
    )


def downgrade() -> None:
    """Drop the knowledge_documents table."""

    op.drop_table("knowledge_documents")