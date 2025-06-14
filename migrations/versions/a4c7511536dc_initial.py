"""initial

Revision ID: a4c7511536dc
Revises: 
Create Date: 2025-06-05 03:47:22.152405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4c7511536dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_keys',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('credits', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('custom_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(length=100), nullable=True),
    sa.Column('feature', sa.String(length=200), nullable=True),
    sa.Column('os_version', sa.String(length=100), nullable=True),
    sa.Column('jailbreak_status', sa.String(length=20), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('contact_info', sa.String(length=200), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('custom_request')
    op.drop_table('api_keys')
    # ### end Alembic commands ###
