from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .user_schema import UserOut
from .barber_schema import BarberOut
from .service_schema import ServiceOut
from .location_schema import LocationOut

class ReviewsCreate(BaseModel):
    user_id: int
    barber_id: int
    rating: int
    review_text: Optional[str] = None
    created_at: datetime

class ReviewsOut(BaseModel):
    review_id: int
    user_id: UserOut
    barber_id: BarberOut
    rating: int
    review_text: Optional[str] = None
    created_at: datetime
