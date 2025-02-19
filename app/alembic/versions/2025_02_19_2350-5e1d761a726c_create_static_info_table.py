"""Create static info table

Revision ID: 5e1d761a726c
Revises: 95b72acda360
Create Date: 2025-02-19 23:50:09.413703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5e1d761a726c"
down_revision: Union[str, None] = "95b72acda360"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "static_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index(op.f("ix_static_info_id"), "static_info", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_static_info_id"), table_name="static_info")
    op.drop_table("static_info")
