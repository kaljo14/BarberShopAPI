from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..security import oauth2
from ..models import models
from ..models.schemas.user_schema import *


def create_crud_router(base_path: str, out_schema, create_schema, update_schema, model,id_column):
    router = APIRouter(
        prefix=f"/{base_path}",
        tags=[f"{base_path.capitalize()}"]
    )

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=out_schema)
    def create_item(item: create_schema, db: Session = Depends(get_db)):
        new_item = model(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @router.get('/', response_model=List[out_schema])
    def get_items(db: Session = Depends(get_db)):
        items = db.query(model).all()
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There are no {model.__name__} defined")
        return items

    @router.get('/{item_id}', response_model=out_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(getattr(model, id_column) == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
        return item

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(get_db),
                    current_user: UserOut = Depends(oauth2.get_current_user)):
        item = db.query(model).filter(getattr(model, id_column) == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")

        if current_user.role_id is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

        db.delete(item)
        db.commit()

    @router.put("/{item_id}", response_model=out_schema)
    def update_item(item_id: int, updated_item: update_schema, db: Session = Depends(get_db),
                    current_user: UserOut = Depends(oauth2.get_current_user)):
        item = db.query(model).filter(getattr(model, id_column) == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")

        if current_user.role_id is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

        update_values = {key: value for key, value in updated_item.dict().items() if value is not None}
        db.query(model).filter(getattr(model, id_column) == item_id).update(update_values, synchronize_session=False)
        db.commit()

        return item

    return router
