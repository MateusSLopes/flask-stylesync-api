from pydantic import BaseModel
from datetime import date

from app.models.model_dump import MongoBaseModel


class Sale(MongoBaseModel, BaseModel):
    sale_date: date
    product_id: str
    quantity: int
    total_value: float