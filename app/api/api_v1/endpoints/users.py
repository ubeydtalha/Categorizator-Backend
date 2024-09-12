


from fastapi import APIRouter

from app.api.database import SessionDep


router =  APIRouter()

# @router.get("/read-all")
# async def get_all_user(session: SessionDep) -> list[User]:
#     return await user.get_all(session)