"""bool on timeslots

Revision ID: 648d6d146c97
Revises: 3bceb1bc732c
Create Date: 2023-10-18 14:07:24.732207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '648d6d146c97'
down_revision = '3bceb1bc732c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeSlots', sa.Column('availabilit', sa.Boolean(), nullable=True))
    op.drop_column('timeSlots', 'availability')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeSlots', sa.Column('availability', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.drop_column('timeSlots', 'availabilit')
    # ### end Alembic commands ###
