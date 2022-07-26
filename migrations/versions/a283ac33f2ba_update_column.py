"""update column

Revision ID: a283ac33f2ba
Revises: 4353a0eed613
Create Date: 2022-08-01 12:41:42.029657

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a283ac33f2ba'
down_revision = '4353a0eed613'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('Format', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('nameCreator', sa.String(length=200), nullable=True),
    sa.Column('note', sa.String(length=200), nullable=False),
    sa.Column('tag', sa.String(length=200), nullable=True),
    sa.Column('status', sa.String(length=200), nullable=True),
    sa.Column('path', sa.String(length=200), nullable=True),
    sa.Column('size', sa.Float(), nullable=False),
    sa.Column('creationDate', sa.DateTime(), nullable=False),
    sa.Column('lastModification', sa.DateTime(), nullable=False),
    sa.Column('nameModificator', sa.String(length=200), nullable=True),
    sa.Column('nameSubCategory', sa.String(length=200), nullable=True),
    sa.Column('nameCategory', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('Format', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('nameCreator', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('note', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('tag', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('path', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('size', mysql.FLOAT(), nullable=False),
    sa.Column('creationDate', mysql.DATETIME(), nullable=False),
    sa.Column('lastModification', mysql.DATETIME(), nullable=False),
    sa.Column('nameModificator', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('nameSubCategory', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('nameCategory', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    # ### end Alembic commands ###
