from pydantic import BaseModel
from datetime import datetime

class TimeSlotCreate(BaseModel):
    barber_id: int
    slot_time: datetime
    availability: str

class TimeSlotOut(BaseModel):
    slot_id: int
    barber_id: int
    slot_time: datetime
    availability: str
