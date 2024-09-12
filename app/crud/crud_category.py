from supabase_py_async import AsyncClient
from app.crud.base import CRUDBase
from app.schemas.auth import UserIn
from app.schemas.category import Category, CategoryCreate, CategoryInDB, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def create(self, db: AsyncClient, *, obj_in: CategoryCreate) -> Category:
        return await super().create(db, obj_in=obj_in)
    async def get(self, db: AsyncClient, *, id: str) -> Category | None:
        return await super().get(db, id=id)

    async def get_all(self, db: AsyncClient) -> list[Category]:
        return await super().get_all(db)

    async def get_multi_by_owner(self, db: AsyncClient, *, user: UserIn) -> list[Category]:
        return await super().get_multi_by_owner(db, user=user)
    
    async def get_multi_by_team(self, db: AsyncClient, *, team_id: str) -> list[Category]:
        return await super().get_multi_by_team(db, team_id=team_id)

    async def update(self, db: AsyncClient, *, obj_in: CategoryUpdate) -> Category:
        return await super().update(db, obj_in=obj_in)

    async def delete(self, db: AsyncClient, *, id: str) -> Category:
        return await super().delete(db, id=id)


category = CRUDCategory(Category)