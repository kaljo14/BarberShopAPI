from datetime import datetime
from typing import Optional,List

from pydantic import BaseModel


class AppointmentsCreate(BaseModel):
    user_id: int
    barber_id: int
    service_id: int
    location_id: int
    appointment_time: datetime
    status: str
    special_request: str


class AppointmentsOut(BaseModel):
    appointment_id: int
    user_id: int
    barber_id: int
    service_id: int
    location_id: int
    appointment_time: datetime
    status: Optional[str] = None
    special_request: Optional[str] = None

    class Config:
        orm_mode = True



class TimeSlot(BaseModel):
    slot_id: int
    barber_id: int


class AppointmentsBooking(BaseModel):
    user_id: int
    barber_id: int
    service_id: int
    location_id: int
    time_slots: List[TimeSlot]
    appointment_time: Optional[datetime] = None
    status: Optional[str] = None
    special_request: Optional[str] = None