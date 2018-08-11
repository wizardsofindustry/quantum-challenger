"""initial revision

Revision ID: 42edb201c9bf
Revises: 
Create Date: 2018-08-11 06:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sq.ext.rdbms.types


# revision identifiers, used by Alembic.
revision = '42edb201c9bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phonenumberchallenges',
    sa.Column('phonenumber', sa.String(), nullable=False),
    sa.Column('challenged', sa.BigInteger(), nullable=False),
    sa.Column('using', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('phonenumber')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phonenumberchallenges')
    # ### end Alembic commands ###
