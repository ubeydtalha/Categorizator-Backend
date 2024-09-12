import logging
from typing import Generic, TypeVar

from supabase_py_async import AsyncClient

from ..schemas.auth import UserIn
from ..schemas.base import CreateBase, ResponseBase, UpdateBase

ModelType = TypeVar("ModelType", bound=ResponseBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateBase)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, db: AsyncClient, *, id: str) -> ModelType | None:
        """get by table_name by id"""
        data, count = (
            await db.table(self.model.table_name).select("*").eq("id", id).execute()
        )
        _, got = data
        return self.model(**got[0]) if got else None

    async def get_all(self, db: AsyncClient) -> list[ModelType]:
        """get all by table_name"""
        data, count = await db.table(self.model.table_name).select("*").execute()
        _, got = data
        return [self.model(**item) for item in got]

    async def get_multi_by_owner(
        self, db: AsyncClient, *, user: UserIn
    ) -> list[ModelType]:
        """get by owner,use it  if rls failed to use"""
        data, count = (
            await db.table(self.model.table_name)
            .select("*")
            .eq("user_id", user.id)
            .eq("team_id", "00000000-0000-0000-0000-000000000000")
            .execute()
        )
        _, got = data
        return [self.model(**item) for item in got]
    
    async def get_multi_by_category(
        self, db: AsyncClient, *, category_id: str
    ) -> list[ModelType]:
        """get by category_id"""
        data, count = (
            await db.table(self.model.table_name)
            .select("*")
            .eq("category_id", category_id)
            .execute()
        )
        _, got = data
        return [self.model(**item) for item in got]
    
    async def get_multi_by_team(
        self, db: AsyncClient, *, team_id: str
    ) -> list[ModelType]:
        """get by team_id"""
        data, count = (
            await db.table(self.model.table_name)
            .select("*")
            .eq("team_id", team_id)
            .execute()
        )
        _, got = data
        return [self.model(**item) for item in got]
    
    async def create(self, db: AsyncClient, *, obj_in: CreateSchemaType) -> ModelType:
        """create by CreateSchemaType"""
        dumped_model = obj_in.model_dump()
        try:
            
            data, count = await db.table(self.model.table_name).insert(dumped_model).execute()
            _, created = data
            if not created:
                raise Exception("Failed to create")
            return self.model(**created[0])
        except Exception as e:
            logging.error(str(e))
            return None

    async def update(self, db: AsyncClient, *, obj_in: UpdateSchemaType) -> ModelType:
        """update by UpdateSchemaType"""
        data, count = (
            await db.table(self.model.table_name)
            .update(obj_in.model_dump())
            .eq("id", obj_in.id)
            .execute()
        )
        _, updated = data
        return self.model(**updated[0])

    async def delete(self, db: AsyncClient, *, id: str) -> ModelType:
        """remove by UpdateSchemaType"""
        data, count = (
            await db.table(self.model.table_name).delete().eq("id", id).execute()
        )
        _, deleted = data
        return self.model(**deleted[0])
