"""auto_votes

Revision ID: 22f86b5acb9c
Revises: f80ec3a4809f
Create Date: 2023-04-01 16:42:41.347203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f86b5acb9c'
down_revision = 'f80ec3a4809f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('posts', 'own_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))
    op.alter_column('posts', 'own_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('posts', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_table('vote')
    # ### end Alembic commands ###
