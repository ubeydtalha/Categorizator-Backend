from fastapi import APIRouter

from app.api.database import CurrentUser, SessionDep
from app.crud.crud_favorite import favorite
from app.schemas.favorite import Favorite, FavoriteCreate


router = APIRouter()

@router.post("/create")
async def create_favorite(favorite_in: FavoriteCreate, session: SessionDep) -> Favorite:
    return await favorite.create(session, obj_in=favorite_in)

@router.get("/read-all-favorite")
async def read_favorites(session: SessionDep) -> list[Favorite]:
    return await favorite.get_all(session)

@router.get("/get-by-id/{id}")
async def read_favorite_by_id(id: str, session: SessionDep) -> Favorite | None:
    return await favorite.get(session, id=id)

@router.get("/get-by-owner")
async def read_favorite_by_owner(session: SessionDep, user: CurrentUser) -> list[Favorite]:
    return await favorite.get_multi_by_owner(session, user=user)

# @router.put("/update-favorite")
# async def update_favorite(favorite_in: FavoriteUpdate, session: SessionDep) -> Favorite:
#     return await favorite.update(session, obj_in=favorite_in)

@router.delete("/delete/{id}")
async def delete_favorite(id: str, session: SessionDep) -> Favorite:
    return await favorite.delete(session, id=id)
