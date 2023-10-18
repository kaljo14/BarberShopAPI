from datetime import datetime, timedelta
# from ..models import models
from ..models import models
from sqlalchemy.orm import Session
from ..database.database import get_db
from fastapi import Depends
from .utils import get_barbers
from ..database.database import SessionLocal 







def generate_and_insert_time_slots(num_days: int):
    db = SessionLocal()
    time_slots = []
    barbers = get_barbers()
    try:
        current_date = datetime.now().date()
        for day in range(num_days):
            start_time = datetime.combine(current_date, datetime.strptime('10:00:00', '%H:%M:%S').time())
            end_time = datetime.combine(current_date, datetime.strptime('18:00:00', '%H:%M:%S').time())
            
            for barber in barbers:
                id = barber.barber_id
                current_time = start_time
                time_interval = timedelta(minutes=15)  # Define time_interval here for clarity
                while current_time < end_time:
                    end_slot = current_time + time_interval
                    time_slot = models.TimeSlot(barber_id=id, start_time=current_time, end_time=end_slot, availability=True)
                    db.add(time_slot)
                    current_time = end_slot

            # Move to the next day
            current_date += timedelta(days=1)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()