"""Create cart table

Revision ID: 589c8197911f
Revises: d7910da497fd
Create Date: 2025-02-17 23:09:34.650253

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "589c8197911f"
down_revision: Union[str, None] = "d7910da497fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_carts_id"), "carts", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_carts_id"), table_name="carts")
    op.drop_table("carts")
