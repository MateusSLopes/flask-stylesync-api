from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

from app.models.model_dump import MongoBaseModel


class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ProductDBModel(MongoBaseModel, Product):
    pass

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None