from supabase_py_async import AsyncClient
from app.crud.base import CRUDBase
from app.schemas.auth import UserIn
from app.schemas.favorite import Favorite, FavoriteCreate, FavoriteInDB, FavoriteUpdate


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteUpdate]):
    async def create(self, db: AsyncClient, *, obj_in: FavoriteCreate) -> Favorite:
        return await super().create(db, obj_in=obj_in)
    
    async def get(self, db: AsyncClient, *, id: str) -> Favorite | None:
        return await super().get(db, id=id)

    # async def get_all(self, db: AsyncClient) -> list[Favorite]:
    #     return await super().get_all(db)

    async def get_multi_by_owner(self, db: AsyncClient, *, user: UserIn) -> list[Favorite]:
        return await super().get_multi_by_owner(db, user=user)
    
    # async def get_multi_by_team(self, db: AsyncClient, *, team_id: str) -> list[Favorite]:
    #     return await super().get_multi_by_team(db, team_id=team_id)

    async def update(self, db: AsyncClient, *, obj_in: FavoriteUpdate) -> Favorite:
        return await super().update(db, obj_in=obj_in)

    async def delete(self, db: AsyncClient, *, id: str) -> Favorite:
        return await super().delete(db, id=id)
    

favorite = CRUDFavorite(Favorite)