from pydantic import BaseModel, EmailStr,constr,validator
from datetime import datetime
from typing import Optional

from pydantic.types import conint




class UserOut(BaseModel):
    user_id: int
    first_name:str
    last_name:str
    role_id:Optional[int] = None
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name:str
    phone_number: constr(min_length=10, max_length=12)
    last_name:str
    role_id:Optional[int] = None
    
    @validator("phone_number")
    def validate_phone_number(cls, phone_number):
        # Check if the phone number contains only numeric characters
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only numeric characters")
        return phone_number



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)