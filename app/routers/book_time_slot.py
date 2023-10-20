from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..models.schemas.appointment_schema import *
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


@router.post("/appp", status_code=status.HTTP_201_CREATED, response_model=AppointmentsOut)
def book_time_slot(appointment: AppointmentsCreate, db: Session = Depends(get_db),
                   current_user: UserCreate = Depends(oauth2.get_current_user)):
    new_item = models.Appointment(**appointment.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
