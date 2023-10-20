# router_manager.py
from fastapi import FastAPI
from .router_config import router_configs
from .crud import create_crud_router


def include_routers_dynamically(app: FastAPI):
    for resource_name, response_model, create_model, update_model, db_model, id_field in router_configs:
        router = create_crud_router(resource_name, response_model, create_model, update_model, db_model, id_field)
        app.include_router(router)
