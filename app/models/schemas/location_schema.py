from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    coordinates: Optional[str] = None


class LocationID(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    class Config:
        orm_mode = True


class LocationOut(LocationCreate):
    location_id: int

    class Config:
        orm_mode = True
