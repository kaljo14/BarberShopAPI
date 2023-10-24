from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..models.schemas.appointment_schema import *
from ..models.schemas.time_slot_schema import TimeSlotID
from ..models.schemas.user_schema import *
from ..security import oauth2
from ..time_manager.utils import *

router = APIRouter(
    prefix="/book_time_slot",
    tags=['Booking']
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_available_time_slots(db: Session = Depends(get_db),
                             current_user: UserCreate = Depends(oauth2.get_current_user)):
    date = datetime(2023, 10, 20)
    return get_consecutive_time_slots(1, date, 3)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[TimeSlotID])
def book_time_slot(time_slots: List[TimeSlotID], db: Session = Depends(get_db),
                   current_user: UserCreate = Depends(oauth2.get_current_user)):
    slot_ids = [timet_slot.slot_id for timet_slot in time_slots]

    existing_slots = db.query(models.TimeSlot).filter(models.TimeSlot.slot_id.in_(slot_ids)).all()

    if len(existing_slots) != len(slot_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Some time slots do not exist")

    for slot in existing_slots:
        slot.update_availability(False)
        db.add(slot)

    db.commit()

    return time_slots


@router.post("/appointments", status_code=status.HTTP_201_CREATED)
def book_time_slot_and_appointment(appointment:AppointmentsBooking, db: Session = Depends(get_db),
                  current_user: UserCreate = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter_by(user_id=appointment.user_id).first()
    service = db.query(models.Service).filter_by(service_id=appointment.service_id).first()
    location = db.query(models.Location).filter_by(location_id=appointment.location_id).first()
    barber = db.query(models.Barber).filter_by(barber_id=appointment.barber_id).first()
    appointment1 = models.Appointment(
    user=user,
    service=service,
    barber=barber,
    location=location,
    appointment_time=datetime.now(),  # Set the appointment time as needed
    status='Scheduled')
    

    # time_slots_data = data.get('timeSlots', [])
    time_slots_data = appointment.time_slots
    
    time_slots = []

    for slot_data in time_slots_data:
        slot_id = slot_data.slot_id
        time_slot = db.query(models.TimeSlot).filter_by(slot_id=slot_id).first()
        if time_slot:
            appointment1.time_slots.append(time_slot)

    
    appointment.time_slots = time_slots

    db.add(appointment1)
    db.commit()
    db.refresh(appointment1)
    
    return appointment1
