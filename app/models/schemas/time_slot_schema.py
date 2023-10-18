from pydantic import BaseModel
from datetime import datetime

class TimeSlotCreate(BaseModel):
    barber_id: int
    start_time:datetime
    end_time: datetime
    availability: bool

class TimeSlotOut(BaseModel):
    slot_id: int
    barber_id: int
    start_time:datetime
    end_time: datetime
    availability: bool
    
    class Config:
        orm_mode = True

class TimeSlotID(BaseModel):
    slot_id: int
    barber_id: int