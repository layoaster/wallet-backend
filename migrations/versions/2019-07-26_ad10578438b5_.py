"""empty message

Revision ID: ad10578438b5
Revises: 
Create Date: 2019-07-26 18:36:21.107807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad10578438b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('transaction_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trans_type', sa.Enum('TRANSFER_OUT', 'TRANSFER_IN', 'DEPOSIT', 'CHARGE', 'WITHDRAWAL', name='transactiontype'), nullable=False),
    sa.Column('amount', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('opening_balance', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('new_balance', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_log')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
