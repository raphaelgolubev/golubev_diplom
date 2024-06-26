"""empty message

Revision ID: a97330a8d2e5
Revises: 534f444d749b
Create Date: 2019-06-05 19:38:50.759273

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a97330a8d2e5'
down_revision = '534f444d749b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('active', sa.String(length=32), nullable=True))
    op.drop_column('profile', 'algorithms')
    op.drop_column('profile', 'country')
    op.drop_column('profile', 'activity')
    op.drop_column('profile', 'language')
    op.drop_column('profile', 'city')
    op.drop_column('profile', 'projects')
    op.drop_column('profile', 'templates')
    op.drop_column('profile', 'scope')
    op.drop_column('profile', 'about')
    op.drop_column('profile', 'username')
    op.add_column('user', sa.Column('user_login', sa.String(length=10), nullable=True))
    op.create_index(op.f('ix_user_user_login'), 'user', ['user_login'], unique=True)
    op.drop_column('user', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', mysql.VARCHAR(length=32), nullable=True))
    op.drop_index(op.f('ix_user_user_login'), table_name='user')
    op.drop_column('user', 'user_login')
    op.add_column('profile', sa.Column('username', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('about', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('scope', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('templates', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('projects', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('city', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('language', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('activity', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('profile', sa.Column('country', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('profile', sa.Column('algorithms', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('profile', 'active')
    # ### end Alembic commands ###
