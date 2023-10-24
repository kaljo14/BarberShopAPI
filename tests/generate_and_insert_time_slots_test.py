from datetime import datetime, timedelta

import pytest

from app.models import models
from app.time_manager.time_slot_creator import generate_and_insert_time_slots


@pytest.mark.parametrize("num_days", [1, 2])  # Test with different values of num_days
def test_generate_and_insert_time_slots(session, num_days,test_barber,test_user2,test_user,test_barber2):
    # Call the function with the specified number of days
    generate_and_insert_time_slots(num_days, session)

    # Perform assertions to check if the time slots were generated and inserted correctly
    # For example, you can check if a specific time slot exists in the database
    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    time_interval = timedelta(minutes=15)

    current_time = start_time
    while current_time < end_time:
        time_slot = session.query(models.TimeSlot).filter_by(start_time=current_time).first()
        print(time_slot.start_time)
        # assert time_slot is not None
        # assert time_slot.availability is True
        current_time += time_interval
