from pydantic import BaseModel
from datetime import datetime

class TimeSlotsCreate(BaseModel):
    barber_id: int
    slot_time: datetime
    availability: str

class TimeSlotsOut(BaseModel):
    slot_id: int
    barber_id: int
    slot_time: datetime
    availability: str
