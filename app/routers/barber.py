from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.user_schema import *
from ..models.schemas.barber_schema import *

from ..security import utils, oauth2
from ..database.database import get_db
from typing import List

router = APIRouter(
    prefix="/barbers",
    tags=['Barbers']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BarberOut)
def create_barber(barber: BarberCreate, db: Session = Depends(get_db),
                  current_user: UserCreate = Depends(oauth2.get_current_user)):
    user_check = db.query(models.User).filter(models.User.user_id == barber.user_id).first()
    if user_check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id:{barber.user_id}")

    barber_existing = db.query(models.Barber).filter(models.Barber.user_id == barber.user_id).first()

    if barber_existing != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The user with id :{barber.user_id}is already registered as a barber")

    new_barber = models.Barber(**barber.dict())
    db.add(new_barber)
    db.commit()
    db.refresh(new_barber)

    return new_barber


@router.get('/', response_model=List[BarberOut])
def get_barbers(db: Session = Depends(get_db), current_user: UserCreate = Depends(oauth2.get_current_user)):
    barbers = db.query(models.Barber).all()
    if not barbers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no barbers defined")

    return barbers


@router.get('/{id}', response_model=BarberOut)
def get_barber(id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(oauth2.get_current_user)):
    barber = db.query(models.Barber).filter(models.Barber.barber_id == id).first()

    if not barber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The barber with the id :{id} does not exist")
    return barber


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_barber(id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(oauth2.get_current_user)):
    barber_query = db.query(models.Barber).filter(models.Barber.barber_id == id)
    barber = barber_query.first()
    if barber == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Barber with id: {id} does not exist")
    print(current_user.role_id)
    if current_user.role_id != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    barber_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=BarberOut)
def update_post(id: int, updated_barber: BarberUpdate, db: Session = Depends(get_db),
                current_user: UserCreate = Depends(oauth2.get_current_user)):
    barber_query = db.query(models.Barber).filter(models.Barber.barber_id == id)
    barber = barber_query.first()

    if barber == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Barber with id: {id} does not exist")

    if current_user.role_id != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    barber_query.update(updated_barber.dict(), synchronize_session=False)

    db.commit()

    return barber_query.first()
