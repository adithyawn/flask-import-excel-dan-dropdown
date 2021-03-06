"""empty message

Revision ID: 774129b43bef
Revises: 
Create Date: 2020-11-22 15:33:40.845794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '774129b43bef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kategori_wbs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_kategori_wbs', sa.String(length=50), nullable=False),
    sa.Column('kategori_wbs', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_kategori_wbs')
    )
    op.create_table('wbs_level2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_wbs_level2', sa.String(length=50), nullable=False),
    sa.Column('wbs_level2', sa.String(length=50), nullable=True),
    sa.Column('id_wbs_spesifik', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_wbs_level2')
    )
    op.create_table('wbs_level3',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_wbs_level3', sa.String(length=50), nullable=False),
    sa.Column('wbs_level3', sa.String(length=50), nullable=True),
    sa.Column('id_wbs_level2', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_wbs_level3')
    )
    op.create_table('wbs_spesifik',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_wbs_spesifik', sa.String(length=50), nullable=False),
    sa.Column('wbs_spesifik', sa.String(length=50), nullable=True),
    sa.Column('id_kategori_wbs', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_wbs_spesifik')
    )
    op.create_table('input_wbs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('input_id_kategori_wbs', sa.String(length=300), nullable=True),
    sa.Column('input_id_wbs_spesifik', sa.String(length=300), nullable=True),
    sa.Column('input_id_wbs_level2', sa.String(length=300), nullable=True),
    sa.Column('input_id_wbs_level3', sa.String(length=300), nullable=True),
    sa.ForeignKeyConstraint(['input_id_kategori_wbs'], ['kategori_wbs.id_kategori_wbs'], ),
    sa.ForeignKeyConstraint(['input_id_wbs_level2'], ['wbs_level2.id_wbs_level2'], ),
    sa.ForeignKeyConstraint(['input_id_wbs_level3'], ['wbs_level3.id_wbs_level3'], ),
    sa.ForeignKeyConstraint(['input_id_wbs_spesifik'], ['wbs_spesifik.id_wbs_spesifik'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('input_wbs')
    op.drop_table('wbs_spesifik')
    op.drop_table('wbs_level3')
    op.drop_table('wbs_level2')
    op.drop_table('kategori_wbs')
    # ### end Alembic commands ###
