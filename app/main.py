from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers.crud import create_crud_router
from .models import models
from .database.database import engine
from .routers import user, auth 
from .config.env_variables_config import settings

from .routers.router_manager import include_routers_dynamically

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


@app.get("/")
def root():
    return {"message": "Personal Project"}
