"""empty message

Revision ID: 5843827a7cf2
Revises: 9008cc589b96
Create Date: 2019-06-02 12:48:18.608509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5843827a7cf2'
down_revision = '9008cc589b96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    # ### end Alembic commands ###
