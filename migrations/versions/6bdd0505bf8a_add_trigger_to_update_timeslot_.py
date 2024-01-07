"""Add trigger to update timeslot availability

Revision ID: 6bdd0505bf8a
Revises: 7f4dcb34ba5b
Create Date: 2023-10-26 16:01:13.597377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bdd0505bf8a'
down_revision = '7f4dcb34ba5b'
branch_labels = None
depends_on = None



def upgrade():
    conn = op.get_bind()
    conn.execute("""
    CREATE OR REPLACE FUNCTION update_timeslot_availability_function()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE "timeSlots"
        SET availability = TRUE
        WHERE slot_id = OLD.time_slot_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    conn.execute("""
    CREATE TRIGGER update_timeslot_availability_after_delete
    AFTER DELETE ON "appointment_timeslot_association"
    FOR EACH ROW
    EXECUTE FUNCTION update_timeslot_availability_function();
    """)

def downgrade():
    conn = op.get_bind()
    conn.execute(f'DROP TRIGGER update_timeslot_availability_after_delete ON "appointment_timeslot_association"')
    conn.execute("DROP FUNCTION update_timeslot_availability_function()")


