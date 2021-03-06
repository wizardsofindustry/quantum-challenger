"""Add purpose column

Revision ID: 9ac8c2a564ec
Revises: 8dff1e470f5f
Create Date: 2018-08-14 19:22:15.570460

"""
from alembic import op
import sqlalchemy as sa
import sq.ext.rdbms.types


# revision identifiers, used by Alembic.
revision = '9ac8c2a564ec'
down_revision = '8dff1e470f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phonenumberchallenges', sa.Column('purpose', sa.String(),
        server_default='SUBJECT_REGISTRATION', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('phonenumberchallenges', 'purpose')
    # ### end Alembic commands ###
