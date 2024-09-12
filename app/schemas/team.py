from datetime import datetime
from pydantic import BaseModel , UUID4, Field
import uuid

from app.utils.helpers import utc_now_str
from .base import ResponseBase, UpdateBase, CreateBase, InDBBase


class Team(ResponseBase):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    created_at: str = Field(default_factory=utc_now_str)
    image : str = Field()
    is_public : bool = Field(default=False)
    edited_at: str = Field(default_factory=utc_now_str)
    user_id : str
    
    table_name = "teams"

    # class Config:
    #     from_attributes = True

class TeamCreate(CreateBase):
    name: str = Field(min_length=1, max_length=100)
    image : str = Field()
    is_public : bool = Field(default=False)
    # edited_at: str = Field(default_factory=utc_now_str)
    user_id : str

    # class Config:

class TeamInDB(InDBBase):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=utc_now_str)
    image : str = Field()
    is_public : bool = Field(default=False)
    edited_at: str = Field(default_factory=utc_now_str)
    user_id : str
    # class Config:

class TeamUpdate(UpdateBase):
    id : str
    name: str = Field(min_length=1, max_length=100)
    image : str = Field()
    is_public : bool = Field(default=False)
    edited_at: str = Field(default_factory=utc_now_str)
    user_id : str
    # class Config: