from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.user_schema import *
from ..models.schemas.time_slot_schema import *
from ..time_manager.utils import *
from ..security import utils, oauth2
from ..database.database import get_db
from typing import List

router = APIRouter(
    prefix="/book_time_slot",
    tags=['Booking']
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_available_time_slots( db: Session = Depends(get_db),current_user: UserCreate = Depends(oauth2.get_current_user)):
    date = datetime(2023, 10, 20) 
    return get_consecutive_time_slots( 1,date,3)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[TimeSlotID])
def book_time_slot(time_slots:List[TimeSlotID], db: Session = Depends(get_db),
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