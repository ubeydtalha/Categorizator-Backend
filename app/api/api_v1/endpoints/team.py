from tkinter import E
from fastapi import APIRouter, Depends

from app.api.database import CurrentUser, SessionDep, get_current_user
from app.crud.crud_teams import Team, TeamCreate, TeamUpdate, UserIn, team
from app.schemas.teams_user import TeamsUserCreate, TeamsRole
from app.crud.crud_teams_user import teams_user

router = APIRouter()


@router.post("/create")
async def create_team(
    team_in: TeamCreate, session: SessionDep, user: CurrentUser
) -> Team:
    response = await team.create(session, obj_in=team_in)

    if not response:
        return {"message": "Team already exists"}

    # Takım oluşturulduktan sonra oluşturan kişiyi admin yapılıyor
    await teams_user.create(
        session,
        obj_in=TeamsUserCreate(
            team_id=response.id, user_id=user.id, role=TeamsRole.OWNER
        ),
    )
    return response


@router.get("/read-all-team")
async def read_teams(session: SessionDep) -> list[Team]:
    """
    Tüm is_public = true olan takımları getirir
    """
    return await team.get_all(session)


@router.get("/get-by-id/{id}")
async def read_team_by_id(id: str, session: SessionDep, user: CurrentUser) -> Team | None:
    """
        Bu isteği atan kullanıcı ya teams_user tablosunda bu takıma kayıtlı olmalı ya da takım public olmalı
    """
    response = (
        await session.table(Team.table_name)
        .select("*")
        .or_(
            filters='is_public.eq.true,teams_user.team_id.eq.teams.id.and.teams_user.user_id.eq.' + user.id
        )
        .execute()
    )
    _, got = response
    return  Team(**got[0]) if got else None


@router.get("/get-by-owner")
async def read_team_by_owner(session: SessionDep, user: CurrentUser) -> list[Team]:
    return await team.get_multi_by_owner(session, user=user)

@router.get("/read-my-teams")
async def read_my_teams(session: SessionDep, user: CurrentUser) -> list[Team]:
    response = (
        await session.table(Team.table_name)
        .select("*,teams_user!inner(user_id)")
        .filter('teams_user.user_id', 'eq', user.id)
        .execute()
    )
    data = response.data
    return [Team(**item) for item in data]


@router.put("/update")
async def update_team(team_in: TeamUpdate, session: SessionDep) -> Team:
    return await team.update(session, obj_in=team_in)


@router.delete("/delete/{id}")
async def delete_team(id: str, session: SessionDep) -> Team:
    return await team.delete(session, id=id)
