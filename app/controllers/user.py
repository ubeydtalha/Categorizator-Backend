from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..main import supabase
from ..schemas import UserCreate, UserInDB, UserUpdate

router = APIRouter()


@router.post("/signup")
async def signup(user: UserCreate):
    # Create a new user in Supabase
    response = await supabase.auth.sign_up(user.email, user.password)
    
    if response["error"]:
        raise HTTPException(status_code=400, detail=response["error"]["message"])
    
    return {"message": "User created successfully"}

@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    # Sign in a user using email and password
    response = await supabase.auth.sign_in_with_password(email=form_data.username, password=form_data.password)
    
    if response["error"]:
        raise HTTPException(status_code=401, detail=response["error"]["message"])
    
    return {"access_token": response["access_token"], "token_type": "bearer"}

@router.post("/signout")
async def signout():
    # Sign out the currently authenticated user
    response = await supabase.auth.sign_out()
    
    if response["error"]:
        raise HTTPException(status_code=400, detail=response["error"]["message"])
    
    return {"message": "User signed out successfully"}


async def get_current_active_user():
    # Get the currently authenticated user from Supabase
    response = await supabase.auth.user()
    
    if response["error"]:
        raise HTTPException(status_code=401, detail=response["error"]["message"])
    
    user = UserInDB(**response["user"])
    
    return user

@router.get("/me")
async def get_current_user(user: UserInDB = Depends(get_current_active_user)):
    # Get the currently authenticated user
    return user

@router.put("/me")
async def update_current_user(user_update: UserUpdate, user: UserInDB = Depends(get_current_active_user)):
    # Update the currently authenticated user
    response = await supabase.auth.update({"email": user.email, "password": user_update.password})
    
    if response["error"]:
        raise HTTPException(status_code=400, detail=response["error"]["message"])
    
    return {"message": "User updated successfully"}