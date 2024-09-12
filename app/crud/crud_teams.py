from supabase_py_async import AsyncClient
from app.crud.base import CRUDBase
from app.schemas.auth import UserIn
from app.schemas.team import Team, TeamCreate, TeamInDB, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    async def create(self, db: AsyncClient, *, obj_in: TeamCreate) -> Team:
        return await super().create(db, obj_in=obj_in)
    
    async def get(self, db: AsyncClient, *, id: str) -> Team | None:
        """
            Eğer takım public değilse ve kullanıcı takımda değilse takımı getirmez
        """
        

        return await super().get(db, id=id)
    
    async def get_all(self, db: AsyncClient) -> list[Team]:
        data, count = await db.table(self.model.table_name).select("*").eq('is_public', True).execute()
        _, got = data
        return [self.model(**item) for item in got]

    async def get_multi_by_owner(self, db: AsyncClient, *, user: UserIn) -> list[Team]:
        """
            Kullanıcının bulunduğu takımları getirir
        """
        data, count = (
            await db.table(self.model.table_name)
            .select("*,teams_user!inner(role)")
            .filter('teams_user.role', 'eq', 'ADMIN'.lower())
            .execute()
        )
        _, got = data

        

        return [self.model(**item) for item in got]

    async def update(self, db: AsyncClient, *, obj_in: TeamUpdate) -> Team:

        return await super().update(db, obj_in=obj_in)

    async def delete(self, db: AsyncClient, *, id: str) -> Team:
        return await super().delete(db, id=id)
    

team = CRUDTeam(Team)