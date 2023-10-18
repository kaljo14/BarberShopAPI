from pydantic import BaseModel, EmailStr,constr,validator
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class LocationCreate(BaseModel):
    name:Optional[str] = None
    address:Optional[str] = None
    phone:Optional[str] = None
    opening_hours:Optional[str] = None
    coordinates:Optional[str] = None

class LocationOut(LocationCreate):
    location_id: int

    class Config:
        orm_mode = True

