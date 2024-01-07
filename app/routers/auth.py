from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import database
from ..models import models
from ..models.schemas import user_schema
from ..security import utils, oauth2
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=user_schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.user_id, "role_id": user.role_id})
    refresh_token = oauth2.create_refresh_token(data={"sub": user.user_id})

    return {"access_token": access_token, "token_type": "bearer" ,"refresh_token": refresh_token}


@router.post('/refresh', response_model=user_schema.Token)
def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = oauth2.verify_token(refresh_token, credentials_exception)
    new_access_token = oauth2.create_access_token(data={"sub": user_id})
    
    return {"access_token": new_access_token, "token_type": "bearer"}