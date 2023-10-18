from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional

class PromotionCreate(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    discount_type: Optional[str] = None
    discount_value: Decimal

class PromotionOut(PromotionCreate):
    promotion_id: int
  