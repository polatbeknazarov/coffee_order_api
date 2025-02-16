"""Create categories table

Revision ID: 8870c87e1944
Revises: 50c0fb3d876c
Create Date: 2025-02-16 03:13:23.995045

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8870c87e1944"
down_revision: Union[str, None] = "50c0fb3d876c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
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
    )
    op.create_index(
        op.f("ix_categories_id"), "categories", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_categories_name"), "categories", ["name"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
