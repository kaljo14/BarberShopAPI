from ..models.models import Barber,Location
from ..database.database import SessionLocal
from ..models.schemas.barber_schema import BarberID

def get_barbers():
    db = SessionLocal()
    barbers_query =db.query(Barber).all()
    barber= [BarberID(barber_id=barber.barber_id, user_id=barber.user_id) for barber in barbers_query]
    return barber

def get_working_time():
    db = SessionLocal()
    barbers_query =db.query(Barber).all()
    barber= [BarberID(barber_id=barber.barber_id, user_id=barber.user_id) for barber in barbers_query]
    return barber
