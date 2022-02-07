"""followers

Revision ID: 95b316bef8bf
Revises: ca0e4d3698b6
Create Date: 2022-02-02 00:42:36.251700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95b316bef8bf'
down_revision = 'ca0e4d3698b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###