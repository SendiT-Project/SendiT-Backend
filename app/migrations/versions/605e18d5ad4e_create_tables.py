"""create tables

Revision ID: 605e18d5ad4e
Revises: 
Create Date: 2023-12-04 02:09:17.659174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '605e18d5ad4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('name_of_parcel', sa.String(), nullable=False),
    sa.Column('destination', sa.String(), nullable=False),
    sa.Column('current_location', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('pickup', sa.String(), nullable=True),
    sa.Column('weight', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('order_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('users')
    # ### end Alembic commands ###