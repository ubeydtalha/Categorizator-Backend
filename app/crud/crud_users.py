from supabase_py_async import AsyncClient
from app.crud.base import CRUDBase

from app.schemas.user import User, UserCreate, UserUpdate

class CRUDUser(CRUDBase):
   
    async def create(self, db: AsyncClient, *, obj_in: UserCreate) -> User:
        return await super().create(db, obj_in=obj_in)
   
    async def get(self, db: AsyncClient, *, id: str) -> User | None:
        return await super().get(db, id=id)
   
    async def get_all(self, db: AsyncClient) -> list[User]:
        return await super().get_all(db)
    
    async def update(self, db: AsyncClient, *, obj_in: UserUpdate) -> User:
        return await super().update(db, obj_in=obj_in)
    
    async def delete(self, db: AsyncClient, *, id: str) -> User:
        return await super().delete(db, id=id)
    
user = CRUDUser(User)
