from datetime import datetime
from pydantic import BaseModel , UUID4, Field
import uuid

from app.utils.helpers import utc_now_str
from .base import ResponseBase, UpdateBase, CreateBase, InDBBase

class Category(ResponseBase):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    order : int = Field(default=0)
    created_at: str = Field(default_factory=utc_now_str)
    image : str = Field()
    user_id : str = Field()
    team_id : str = Field()
    edited_at: str = Field(default_factory=utc_now_str)
    
    table_name = "categories"

    # class Config:
"""
b'{"name":"12312","image":"","order":0,"createdAt":"2024-09-01 15:04:56.742944",
"editedAt":"2024-09-01 15:04:56.742884",
"user_id":"62bc4473-a284-4b72-8970-51f81fac223f",
"team_id":"00000000-0000-0000-0000-000000000000"}'
"""
class CategoryCreate(CreateBase):
    name: str = Field(min_length=1, max_length=100)
    image : str = Field()
    order : int = Field(default=0)
    user_id : str = Field()
    team_id : str = Field()
    created_at: str = Field(default_factory=utc_now_str)
    edited_at: str = Field(default_factory=utc_now_str)

    # class Config:


class CategoryInDB(InDBBase):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    order : int = Field(default=0)
    created_at: str = Field(default_factory=utc_now_str)
    image : str = Field()
    user_id : str = Field()
    team_id : str = Field()
    edited_at: str = Field(default_factory=utc_now_str)
    

    # class Config:

class CategoryUpdate(UpdateBase):
    id : str = Field()
    name: str = Field()
    image : str = Field()
    order : int = Field()
    edited_at: str = Field()

    # class Config:

class CategorySync(BaseModel):
    id : str
    name: str
    order : int
    created_at: str
    image : str
    user_id : str
    team_id : str
    edited_at: str
    dummy_id : str
    is_synced : bool = False

    # class Config: