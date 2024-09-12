from datetime import datetime
from typing import List, Optional
from pydantic import  UUID4, Field

from app.utils.helpers import utc_now_str
from .base import *
import uuid

class Item(ResponseBase):
    # id: UUID4 = Field(default_factory= lambda: uuid.uuid4().hex)
    name: str
    second_name : str 
    description: str
    barcode : str
    price: float
    created_at: datetime 
    image : str 
    images : list 
    user_id : Optional[str] 
    team_id : Optional[str] 
    edited_at: str = Field(default_factory=utc_now_str)
    category_id: Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    quantity: Optional[int] = Field(default=0)
    table_name = "products"


    
    
class ItemCreate(CreateBase):
    name: str = Field(min_length=1, max_length=100)
    second_name : Optional[str] = Field(min_length=0, max_length=100)
    description: Optional[str] = Field(min_length=0, max_length=300)
    barcode : str = Field(default=0)
    price: Optional[float] = Field(default=0.0,ge=-1)
    image : Optional[str] = Field()
    images : Optional[List[str]] = Field()
    user_id : Optional[str] = Field()
    team_id : Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    edited_at: str = Field(default_factory=utc_now_str)
    category_id: Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    quantity: Optional[int] = Field(default=0)

class ItemInDB(InDBBase):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    second_name : str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=300)
    barcode : str = Field(ge=0)
    price: float = Field(ge=0)
    created_at: datetime = Field(default_factory=utc_now_str)
    image : str = Field()
    images : list = Field()
    user_id : Optional[str] = Field()
    team_id : Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    edited_at: str = Field(default_factory=utc_now_str)
    category_id: Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    quantity: int = Field(default=0)

class ItemUpdate(UpdateBase):
    id: str = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=100)
    second_name : str = Field(min_length=0, max_length=100)
    description: str = Field(min_length=0, max_length=300)
    barcode : str = Field()
    price: float = Field()
    image : str = Field()
    images : list = Field()
    # user_id : Optional[str] = Field()
    # team_id : Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    edited_at: str = Field()
    category_id: Optional[str] = Field(default='00000000-0000-0000-0000-000000000000')
    quantity: int = Field(default=0)


class ItemSync(SyncBase):
    id : str
    name : str
    second_name : str
    description: str
    image: str
    images: List[str]
    price: float
    quantity: int
    category_id: str
    barcode: str
    edited_at: str
    created_at: str
    user_id: str
    team_id: str
    dummy_id: str
    is_synced: bool