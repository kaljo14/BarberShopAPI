from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.barber_schema import *
from ..security import utils
from ..database.database  import get_db
from typing import List

router = APIRouter(
    prefix="/barbers",
    tags=['Barbers']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BarberOut)
def create_user(barber: BarberCreate, db: Session = Depends(get_db)):

   
    user_check = db.query(models.User).filter(models.User.user_id == barber.user_id).first()
    if user_check ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no user with id:{barber.user_id}")
    
    barber_existing= db.query(models.Barber).filter(models.Barber.user_id == barber.user_id).first()
    
    if barber_existing != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"The user with id :{barber.user_id}is already registered as a barber")


    new_barber = models.Barber(**barber.dict())
    db.add(new_barber)
    db.commit()
    db.refresh(new_barber)

    return new_barber