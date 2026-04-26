from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.model_dump import MongoBaseModel


class LoginPayload(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(MongoBaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    username: str
