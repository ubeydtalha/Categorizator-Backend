from fastapi import APIRouter

from app.api.database import CurrentUser, SessionDep
from app.crud.crud_category import category
from app.schemas.category import Category, CategoryCreate, CategoryUpdate


router = APIRouter()

@router.post("/create")
async def create_category(category_in: CategoryCreate, session: SessionDep) -> Category:
    return await category.create(session, obj_in=category_in)

@router.get("/read-all")
async def read_categories(session: SessionDep) -> list[Category]:
    return await category.get_all(session)

@router.get("/get-by-id/{id}")
async def read_category_by_id(id: str, session: SessionDep) -> Category | None:
    return await category.get(session, id=id)

@router.get("/get-by-owner")
async def read_category_by_owner(session: SessionDep, user: CurrentUser) -> list[Category]:
    return await category.get_multi_by_owner(session, user=user)

@router.get("/get-by-team/{team_id}")
async def read_category_by_team(team_id: str, session: SessionDep) -> list[Category]:
    return await category.get_multi_by_team(session, team_id=team_id)

@router.put("/update")
async def update_category(category_in: CategoryUpdate, session: SessionDep) -> Category:
    return await category.update(session, obj_in=category_in)

@router.delete("/delete/{id}")
async def delete_category(id: str, session: SessionDep) -> Category:
    return await category.delete(session, id=id)

