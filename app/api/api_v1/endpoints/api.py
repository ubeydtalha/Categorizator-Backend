from fastapi import APIRouter


api_router = APIRouter()

@api_router.get("/check")
async def check():
    return {"message": "Hello World"}