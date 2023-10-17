from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .database.database  import engine
from .routers import user,role,auth,barber
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
app.include_router(role.router)
app.include_router(auth.router)
app.include_router(barber.router)
@app.get("/")
def root():
    return {"message": "Hello World "}
