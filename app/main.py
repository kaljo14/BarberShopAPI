from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .time_manager.time_slot_creator import generate_and_insert_time_slots
from .time_manager.utils import get_barbers,get_consecutive_time_slots
from .routers.crud import create_crud_router
from .models import models
from .database.database import engine
from .routers import user, auth 
from .config.env_variables_config import settings

from .routers.router_manager import include_routers_dynamically


from datetime import datetime

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

include_routers_dynamically(app)
date = datetime(2023, 10, 18) 
# generate_and_insert_time_slots(settings.days_ahead_time_slots_generator)
get_consecutive_time_slots( 1,date,3)

@app.get("/")
def root():
    return {"message": "Personal Project"}
