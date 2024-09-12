
from app.schemas.base import CreateBase, InDBBase, ResponseBase, UpdateBase


class User(ResponseBase):
    id: str
    email: str
    username: str
    full_name: str
    image : str
    created_at: str
    edited_at: str
    auth_id : str
    table_name = "users"

class UserBase(BaseModel):
    id : str
    email: str
    username: str
    full_name: str
    image : str
    created_at: str
    edited_at: str
    auth_id : str

class UserCreate(CreateBase):
    email: str
    username: str
    full_name: str
    image : str
    created_at: str
    edited_at: str
    auth_id : str

class UserInDB(InDBBase):
    id: str
    email: str
    username: str
    full_name: str
    image : str
    created_at: str
    edited_at: str
    auth_id : str

class UserUpdate(UpdateBase):
    id: str
    email: str
    username: str
    full_name: str
    image : str
    created_at: str
    edited_at: str

