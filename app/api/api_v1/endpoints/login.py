
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from supabase_py_async import AsyncClient

from app.api.database import init_super_client, super_client
from app.core.config import settings
from app.schemas.auth import UserIn, UserInDB, UserJWT, UserLogin, UserOut


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.API_V1_STR + "/login/token")
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], super_client: AsyncClient = Depends(init_super_client)):
    
    try:
        auth_response = await super_client.auth.sign_in_with_password(
            {"email": form_data.username, "password": form_data.password}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    
    return {"access_token": auth_response.session.access_token, "token_type": auth_response.session.token_type}


jwt_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.API_V1_STR + "/login/jwt",
    tokenUrl=settings.API_V1_STR + "/login/jwt/token",
)
@router.post("/jwt")
async def login_with_jwt(userJWT: UserJWT, super_client: AsyncClient = Depends(init_super_client)):
    try:
        auth_response = await super_client.auth.set_session(
            access_token=userJWT.access_token,
            refresh_token=userJWT.refresh_token
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unauthorized")
    
    return auth_response



@router.get("/protected-endpoint")
async def protected_endpoint(token: str = Depends(oauth2_scheme)):
    # Bu alanı JWT token doğrulaması yapacak şekilde ayarlayabilirsiniz.
    if token != "your_generated_jwt":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Protected data"}
