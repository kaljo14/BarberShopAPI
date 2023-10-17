from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas import role_schema
from ..database.database  import get_db
from typing import List

router = APIRouter(
    prefix="/roles",
    tags=['Roles']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=role_schema.RoleOut)
def create_user(role: role_schema.RoleCreat, db: Session = Depends(get_db)):

    new_role = models.Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@router.get('/', response_model=List[role_schema.RoleOut])
def get_user( db: Session = Depends(get_db), ):
    role = db.query(models.Role).all()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no roles defined")

    return role