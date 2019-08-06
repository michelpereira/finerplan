"""creates CreditCard as joined table model inheritance based on Account

Revision ID: 8ed2729f60b4
Revises: 362c7b1c7897
Create Date: 2019-08-06 16:56:51.474576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ed2729f60b4'
down_revision = '362c7b1c7897'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('credit_card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('closing', sa.Integer(), nullable=True),
    sa.Column('payment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('type')

    op.drop_table('credit_card')
    # ### end Alembic commands ###
