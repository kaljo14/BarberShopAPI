from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.schemas.barber_schema import BarberCreate, BarberUpdate, BarberOut
from .models.schemas.role_schema import RoleOut, RoleCreat
from .models.schemas.user_schema import UserCreate, UserUpdate, UserOut
from .routers.crud import create_crud_router
from .models import models
from .database.database import engine
from .routers import user, role, auth, barber, location, services
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
# app.include_router(role.router)
app.include_router(auth.router)
app.include_router(barber.router)
# app.include_router(location.router)
# app.include_router(services.router)


# user_router = create_crud_router("users", UserOut, UserCreate, UserUpdate, models.User, "user_id")
# app.include_router(user_router)
#
# barber_router = create_crud_router("barbers", BarberOut, BarberCreate, BarberUpdate, models.Barber, "barber_id")
# app.include_router(barber_router)
role_router = create_crud_router("roles", RoleOut, RoleCreat, RoleCreat, models.Role, "role_id")
app.include_router(role_router)


@app.get("/")
def root():
    return {"message": "Hello World "}
