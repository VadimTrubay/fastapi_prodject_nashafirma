"""Init

Revision ID: eef52485ad29
Revises: 28b2d4ff9b3d
Create Date: 2024-02-02 01:18:10.439716

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eef52485ad29"
down_revision: Union[str, None] = "28b2d4ff9b3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("items", sa.Column("order_id", sa.Integer(), nullable=True))
    op.add_column("items", sa.Column("product_id", sa.Integer(), nullable=True))
    op.drop_constraint("items_order_fkey", "items", type_="foreignkey")
    op.drop_constraint("items_product_fkey", "items", type_="foreignkey")
    op.create_foreign_key(
        None, "items", "products", ["product_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "items", "orders", ["order_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("items", "order")
    op.drop_column("items", "product")
    op.add_column("orders", sa.Column("user_id", sa.Integer(), nullable=True))
    op.drop_constraint("orders_user_fkey", "orders", type_="foreignkey")
    op.create_foreign_key(
        None, "orders", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("orders", "user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "orders", sa.Column("user", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "orders", type_="foreignkey")
    op.create_foreign_key(
        "orders_user_fkey", "orders", "users", ["user"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("orders", "user_id")
    op.add_column(
        "items", sa.Column("product", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "items", sa.Column("order", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "items", type_="foreignkey")
    op.drop_constraint(None, "items", type_="foreignkey")
    op.create_foreign_key(
        "items_product_fkey",
        "items",
        "products",
        ["product"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "items_order_fkey", "items", "orders", ["order"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("items", "product_id")
    op.drop_column("items", "order_id")
    # ### end Alembic commands ###
