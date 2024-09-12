from supabase_py_async import AsyncClient
from app.crud.base import CRUDBase
from app.schemas.auth import UserIn
from app.schemas.teams_user import TeamsUser, TeamsUserCreate, TeamsUserInDB, TeamsUserUpdate


class CRUDTeamsUser(CRUDBase[TeamsUser, TeamsUserCreate, TeamsUserUpdate]):
    async def create(self, db: AsyncClient, *, obj_in: TeamsUserCreate) -> TeamsUser:
        return await super().create(db, obj_in=obj_in)
    
    async def get(self, db: AsyncClient, *, id: str) -> TeamsUser | None:
        return await super().get(db, id=id)
    
    async def get_multi_by_team(self, db: AsyncClient, *, team_id: str) -> list[TeamsUser]:
        """
            Takımdaki kullanıcıları getirir
        """
        return await super().get_multi_by_team(db, team_id=team_id)

    async def update(self, db: AsyncClient, *, obj_in: TeamsUserUpdate) -> TeamsUser:
        """
            Kullanıcının rolünü günceller
        """
        return await super().update(db, obj_in=obj_in)

    async def delete(self, db: AsyncClient, *, id: str) -> TeamsUser:
        """
            Kullanıcıyı takımdan çıkarır
        """
        return await super().delete(db, id=id)
    
    async def get_multi_by_user(self, db: AsyncClient, *, user_id: str) -> list[TeamsUser]:
        """
            Kullanıcının takımlarını getirir
        """
        data, count = await db.table(self.model.table_name).select("*").eq("user_id", user_id).execute()
        _, got = data
        return [self.model(**item) for item in got]
    

teams_user = CRUDTeamsUser(TeamsUser)