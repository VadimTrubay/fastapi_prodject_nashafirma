"""last2

Revision ID: 28b2d4ff9b3d
Revises: 6ee629690dc8
Create Date: 2024-01-28 22:43:01.980922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28b2d4ff9b3d'
down_revision: Union[str, None] = '6ee629690dc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('order', sa.Integer(), nullable=True))
    op.add_column('items', sa.Column('product', sa.Integer(), nullable=True))
    op.drop_constraint('items_order_id_fkey', 'items', type_='foreignkey')
    op.drop_constraint('items_product_id_fkey', 'items', type_='foreignkey')
    op.create_foreign_key(None, 'items', 'products', ['product'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'items', 'orders', ['order'], ['id'], ondelete='CASCADE')
    op.drop_column('items', 'order_id')
    op.drop_column('items', 'product_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('items', sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.create_foreign_key('items_product_id_fkey', 'items', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('items_order_id_fkey', 'items', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.drop_column('items', 'product')
    op.drop_column('items', 'order')
    # ### end Alembic commands ###