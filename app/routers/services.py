from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import models
from ..models.schemas import role_schema,user_schema
from ..database.database  import get_db
from typing import List
from ..security import oauth2

router = APIRouter(
    prefix="/services",
    tags=['Services']
)
