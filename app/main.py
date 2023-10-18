from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.schemas.barber_schema import BarberCreate, BarberUpdate, BarberOut
from .models.schemas.role_schema import RoleOut, RoleCreate
from .models.schemas.user_schema import UserCreate, UserUpdate, UserOut
from .models.schemas.location_schema import *
from .models.schemas.service_schema import *
from .models.schemas.inventory_schema import *
from .models.schemas.appointment_schema import *
from .models.schemas.review_schema import *
from .models.schemas.promotion_schema import *
from .models.schemas.time_slot_schema import *
from .routers.crud import create_crud_router
from .models import models
from .database.database import engine
from .routers import user, auth 
from .config.env_variables_config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)




barber_router = create_crud_router("barbers", BarberOut, BarberCreate, BarberUpdate, models.Barber, "barber_id")
app.include_router(barber_router)

role_router = create_crud_router("roles", RoleOut, RoleCreate, RoleCreate, models.Role, "role_id")
app.include_router(role_router)

location_router = create_crud_router("location", LocationOut, LocationCreate, LocationCreate, models.Location, "location_id")
app.include_router(location_router)

services_router = create_crud_router("services", ServiceOut, ServiceCreate, ServiceCreate, models.Service, "service_id")
app.include_router(services_router)

inventory_router = create_crud_router("inventory", InventoryOut, InventoryCreate, InventoryCreate, models.Inventory, "inventory_id")
app.include_router(inventory_router)

appointments_router = create_crud_router("appointments", AppointmentsOut, AppointmentsCreate, AppointmentsCreate, models.Appointment, "appointments_id")
app.include_router(appointments_router)

review_router = create_crud_router("review", ReviewOut, ReviewCreate, ReviewCreate, models.Review, "review_id")
app.include_router(review_router)

promotion_router = create_crud_router("promotion", PromotionOut, PromotionCreate, PromotionCreate, models.Promotion, "promotion_id")
app.include_router(promotion_router)

timeSlot_router = create_crud_router("timeSlot", TimeSlotOut, TimeSlotCreate, TimeSlotCreate, models.TimeSlot, "slot_id")
app.include_router(timeSlot_router)

@app.get("/")
def root():
    return {"message": "Personal Project"}
