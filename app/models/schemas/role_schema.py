from pydantic import BaseModel, EmailStr,constr,validator
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class RoleOut(BaseModel):
    role_id: int
    role_name:str
    
    class Config:
        orm_mode = True

class RoleCreat(BaseModel):
    role_name:str

    class Config:
        orm_mode = True