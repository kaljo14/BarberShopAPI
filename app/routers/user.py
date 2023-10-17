from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas import schemas
from ..security import utils
from ..database.database  import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{user_id}', response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} does not exist")

    return user


