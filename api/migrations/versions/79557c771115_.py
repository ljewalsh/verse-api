"""empty message

Revision ID: 79557c771115
Revises: 4ced62fe5132
Create Date: 2019-11-05 14:38:06.281812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79557c771115'
down_revision = '4ced62fe5132'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_account_id', sa.Integer(), nullable=False),
    sa.Column('to_account_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['from_account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['to_account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###