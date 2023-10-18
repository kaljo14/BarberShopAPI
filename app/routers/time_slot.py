from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,Query
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.user_schema import *

from ..models.schemas.time_slot_schema import *
from ..security import utils, oauth2
from ..database.database import get_db
from typing import List

router = APIRouter(
    prefix="/getTimeSlot",
    tags=['getTimeSlot']
)


@router.get('/', response_model=List[TimeSlotOut])
def get_barbers(
    db: Session = Depends(get_db), current_user: UserCreate = Depends(oauth2.get_current_user),
    barber_id: int = Query(default=None),
    num_of_timeslots: int = Query(default=None),
    ):
    timeSlots = db.query(models.TimeSlot).filter(models.TimeSlot.barber_id == barber_id ).all()
    if not barbers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no barbers defined")

    return barbers
 user_query = db.query(models.User).filter(models.User.user_id == id)
    user = user_query.first()


