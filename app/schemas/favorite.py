from datetime import datetime
from pydantic import BaseModel , UUID4, Field
import uuid

from app.utils.helpers import utc_now_str
from .base import ResponseBase, UpdateBase, CreateBase, InDBBase


class Favorite(ResponseBase):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    user_id: str
    product_id: str
    created_at: datetime = Field(default_factory=utc_now_str)
    edited_at: str = Field(default_factory=utc_now_str)
    
    table_name = "favorites"

    # class Config:

class FavoriteCreate(CreateBase):
    user_id: str
    product_id: str
    edited_at: str = Field(default_factory=utc_now_str)
    

    # class Config:

class FavoriteInDB(InDBBase):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    user_id: str
    product_id: str
    created_at: datetime = Field(default_factory=utc_now_str)
    edited_at: str = Field(default_factory=utc_now_str)

    # class Config:

class FavoriteUpdate(UpdateBase):
    user_id: str
    product_id: str
    edited_at: str = Field(default_factory=utc_now_str)

    # class Config:

    