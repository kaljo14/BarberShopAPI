from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic.types import conint

class ServiceCreat(BaseModel):
    name: str
    duration: int
    price: Decimal
    location_id: int

class ServiceOut(ServiceCreat):
    service_id: int
    
    class Config:
        orm_mode = True


