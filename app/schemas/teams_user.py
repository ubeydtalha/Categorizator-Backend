from datetime import datetime
from enum import Enum
from pydantic import BaseModel , Field

from app.schemas.base import ResponseBase
from app.utils.helpers import utc_now_str 

class TeamsRole(Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"
    OWNER = "owner"
    CANDIDATE = "candidate"



class TeamsUser(ResponseBase):
    id: str = Field()
    user_id: str = Field()
    team_id: str = Field()
    created_at: str = Field(default_factory=utc_now_str)
    role : str = Field(default=TeamsRole.USER)
    edited_at: str = Field(default_factory=utc_now_str)
    table_name = "teams_user"


class TeamsUserCreate(BaseModel):
    user_id: str = Field()
    team_id: str = Field()
    role : str = Field(default=TeamsRole.USER)
    edited_at: str = Field(default_factory=utc_now_str)
    

class TeamsUserInDB(BaseModel):
    id: str = Field()
    user_id: str = Field()
    team_id: str = Field()
    created_at: datetime = Field(default_factory=utc_now_str)
    role : str = Field(default=TeamsRole.USER)
    edited_at: str = Field(default_factory=utc_now_str)
    

class TeamsUserUpdate(BaseModel):
    id: str = Field()
    user_id: str = Field()
    team_id: str = Field()
    role : str = Field(default=TeamsRole.USER)
    edited_at: str = Field(default_factory=utc_now_str)
    

