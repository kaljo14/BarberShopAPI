"""create users table

Revision ID: 04aff0612ae9
Revises: 
Create Date: 2023-10-16 16:41:56.680196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04aff0612ae9'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_table('users')
    pass