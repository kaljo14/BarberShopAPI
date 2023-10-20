from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .barber_schema import BarberOut
from .user_schema import UserOut


class ReviewCreate(BaseModel):
    user_id: int
    barber_id: int
    rating: int
    review_text: Optional[str] = None
    created_at: datetime


class ReviewOut(BaseModel):
    review_id: int
    user_id: UserOut
    barber_id: BarberOut
    rating: int
    review_text: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
