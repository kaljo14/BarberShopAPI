from pydantic import BaseModel
from datetime import date

class InventoryCreate(BaseModel):
    location_id: int
    product_name: str
    quantity: int
    last_restocked: date

class InventoryOut(InventoryCreate):
    inventory_id: int
    