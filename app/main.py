from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.env_variables_config import settings
from .database.database import engine
from .models import models
from .routers import user, auth, book_time_slot
from .routers.router_manager import include_routers_dynamically
from .time_manager.time_slot_creator import generate_and_insert_time_slots

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
app.include_router(book_time_slot.router)

include_routers_dynamically(app)
date = datetime(2023, 10, 20)
# generate_and_insert_time_slots(settings.days_ahead_time_slots_generator,)


# x = get_consecutive_time_slots( 1,date,3)
# print (x)
# get_working_hours(1)
# get_all_barbers(1)
# x = [
#     {"slot_id": 3329, "barber_id": 1},
#     {"slot_id": 3330, "barber_id": 1},
#     {"slot_id": 3331, "barber_id": 1}
# ]
# working_hours = get_working_hours(1)
# print(working_hours)

@app.get("/")
def root():
    return {"message": "Personal Project"}
