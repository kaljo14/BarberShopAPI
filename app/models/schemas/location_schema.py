from pydantic import BaseModel, EmailStr,constr,validator
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class LocationCreat(BaseModel):
    name:Optional[str] = None
    address:Optional[str] = None
    phone:Optional[str] = None
    opening_hours:Optional[str] = None
    coordinates:Optional[str] = None

class LocationOut(LocationCreat):
    location_id: int

    class Config:
        orm_mode = True

