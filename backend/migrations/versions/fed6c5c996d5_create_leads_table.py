from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fed6c5c996d5'
down_revision = "e05b79bd6b36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "service",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "location",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "urgency",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "problem",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "budget",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "customer_intent",
            sa.String(length=200),
            nullable=True,
        ),
        sa.Column(
            "lead_priority",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'NEW'"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("leads")