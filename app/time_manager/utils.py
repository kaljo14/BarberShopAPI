from ..models.models import Barber,Location
from ..database.database import SessionLocal
from ..models.schemas.barber_schema import BarberID
from ..models.schemas.location_schema import LocationID
from ..models.schemas.time_slot_schema import TimeSlotID
from ..models.models import TimeSlot


from datetime import datetime, timedelta

def get_all_barbers(location_id: int):
    db = SessionLocal()
    barbers_query =db.query(Barber).filter(Barber.location_id == location_id).all()
    barber= [BarberID(barber_id=barber.barber_id, user_id=barber.user_id) for barber in barbers_query]
    return barber

def get_working_hours(location_id: int):
    db = SessionLocal()
    location_query =db.query(Location).filter(Location.location_id ==location_id).all()
    print(location_query)
    working_hours= [LocationID( start_time=location.start_time ,end_time=location.end_time) for location in location_query]
    print(working_hours)
    # print("Start Time:", working_hours[0].start_time)
    return working_hours



def get_consecutive_time_slots( barber_id: int, date: datetime, number_of_timeslots: int):
    # Calculate the start and end times for the given date
    working_hours=get_working_hours(1)
    db = SessionLocal()
    start_time = datetime(date.year, date.month, date.day, 7, 0, 0)  # Assuming 10:00 AM is the start time
    end_time = datetime(date.year, date.month, date.day, 18, 0, 0)   # Assuming 6:00 PM is the end time

    # Retrieve available time slots for the given barber on the specified date
    available_time_slots = db.query(TimeSlot) \
        .filter(TimeSlot.barber_id == barber_id) \
        .filter(TimeSlot.start_time >= start_time) \
        .filter(TimeSlot.end_time <= end_time) \
        .filter(TimeSlot.availability == True) \
        .order_by(TimeSlot.start_time) \
        .all()

    
    consecutive_time_slots_pairs = []
    current_consecutive_slots = []

    for time_slot in available_time_slots:
        # Check if the current time slot is consecutive to the previous one
        if not current_consecutive_slots or time_slot.start_time == current_consecutive_slots[-1].end_time:
            current_consecutive_slots.append(time_slot)
        else:
            current_consecutive_slots = [time_slot]

        # Check if we have a pair with the desired number of time slots
        if len(current_consecutive_slots) == number_of_timeslots:
            consecutive_time_slots_pairs.append(current_consecutive_slots.copy())
            current_consecutive_slots = []
    # consecutive= [TimeSlotID(barber_id=consecutive.barber_id, slot_id=consecutive.slot_id) for consecutive in consecutive_time_slots_pairs]  
    # print (consecutive)

    print(len(consecutive_time_slots_pairs))
    for i, group in enumerate(consecutive_time_slots_pairs):
        print(f"Group {i + 1}:")
        for time_slot in group:
            print(f"TimeSlotID(slot_id={time_slot.slot_id}, barber_id={time_slot.barber_id})")

   
    
    return consecutive_time_slots_pairs