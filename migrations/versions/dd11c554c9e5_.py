"""empty message

Revision ID: dd11c554c9e5
Revises: 7d55bd61980f
Create Date: 2017-11-30 02:22:19.628185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd11c554c9e5'
down_revision = '7d55bd61980f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('header', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'header')
    # ### end Alembic commands ###