from decimal import Decimal

from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    duration: int
    price: Decimal
    location_id: int


class ServiceOut(ServiceCreate):
    service_id: int

    class Config:
        orm_mode = True
