from typing import Hashable
from gotrue import User, UserAttributes
from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserJWT(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    # providerToken: str
    # providerRefreshToken : str

class UserMetaData(BaseModel):
    profile_image_url: str | None = None
    full_name: str | None = None
    username : str | None = None

# Shared properties
class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


# request
class UserIn(Token, User):
    user_metadata: UserMetaData | None = None
    pass


# Properties to receive via API on creation
# in
class UserCreate(BaseModel):
    
    pass


# Properties to receive via API on update
# in
class UserUpdate(UserAttributes):
    pass


# response


class UserInDBBase(BaseModel):
    pass


# Properties to return to client via api
# out
class UserOut(Token):
    pass


# Properties properties stored in DB
class UserInDB(User):
    pass

class User(
    UserIn,
    UserOut,
    UserInDB,
    UserMetaData,
    Token
):
    pass
