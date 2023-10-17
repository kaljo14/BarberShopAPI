from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.location_schema import *
from ..models.schemas.user_schema import *
from ..database.database  import get_db
from typing import List
from ..security import oauth2

router = APIRouter(
    prefix="/locations",
    tags=['Locations']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=LocationOut)
def create_location(location:LocationCreat,db: Session = Depends(get_db),current_user: UserCreate =Depends(oauth2.get_current_user)):
    new_location = models.Location(**location.dict())
    
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


@router.get('/', response_model=List[LocationOut])
def get_user( db: Session = Depends(get_db), current_user: UserCreate =Depends(oauth2.get_current_user) ):
  
    locations = db.query(models.Location).all()
    # example for future use for the user model 
    print(current_user.user_id)

    if not locations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no locations defined")

    return locations