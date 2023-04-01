"""auto_users

Revision ID: 13e4b73c91e4
Revises: ef9b82608d60
Create Date: 2023-04-01 16:38:11.059406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13e4b73c91e4'
down_revision = 'ef9b82608d60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_table('users')
    # ### end Alembic commands ###
