"""auto_add_fk_posts

Revision ID: f80ec3a4809f
Revises: 13e4b73c91e4
Create Date: 2023-04-01 16:40:16.058523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f80ec3a4809f'
down_revision = '13e4b73c91e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('own_id', sa.Integer(), nullable=False))
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.create_foreign_key(None, 'posts', 'users', ['own_id'], ['id'], ondelete='CASCADE')
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_column('posts', 'own_id')
    # ### end Alembic commands ###
