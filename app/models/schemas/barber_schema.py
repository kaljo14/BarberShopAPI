from pydantic import BaseModel, EmailStr,constr,validator
from datetime import datetime
from typing import Optional
from .user_schema import UserOut

from pydantic.types import conint

class BarberOut(BaseModel):
    barber_id:int
    user_id:int
    specialization:Optional[str] = None
    location_id:Optional[int] = None
    bio:Optional[str] = None
    user: UserOut

    class Config:
        orm_mode = True

class BarberCreate(BaseModel):
    user_id:int
    specialization:Optional[str] = None
    location_id:Optional[int] = None
    bio:Optional[str] = None

class BarberUpdate(BaseModel):
    specialization:Optional[str] = None
    location_id:Optional[int] = None
    bio:Optional[str] = None