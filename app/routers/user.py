from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas.user_schema import *
from ..security import utils, oauth2
from ..database.database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter_by(phone_number=models.User.phone_number).first()
    if existing_user:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with this phone number already exists.")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Handle other potential integrity issues
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There was a problem with creating the user.")

    # Refresh to get the new user data from the database
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=List[UserOut])
def get_user(db: Session = Depends(get_db), ):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no users defined")

    return users


@router.get('/{user_id}', response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} does not exist")

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.user_id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    print(current_user.role_id)
    if current_user.role_id is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=UserOut)
def update_post(id: int, updated_user: UserUpdate, db: Session = Depends(get_db),
                current_user: UserCreate = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.user_id == id)
    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    print(current_user.user_id)
    if current_user.role_id is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    update_values = {key: value for key, value in updated_user.dict().items() if value is not None}

    user_query.filter(models.User.user_id == id).update(update_values, synchronize_session=False)
    # user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()
