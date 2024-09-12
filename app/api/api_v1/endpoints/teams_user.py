

from fastapi import APIRouter

from app.api.database import SessionDep
from app.schemas.teams_user import TeamsUser, TeamsUserCreate, TeamsUserInDB
from app.crud.crud_teams_user import teams_user

router = APIRouter()


@router.get("/invite-autocomplete")
async def invite_autocomplete(session: SessionDep, search_text : str) -> list[dict]:
    """
        Kullanıcı arama
    """
    response = await session.rpc('autocomplete_users', {'search_text': search_text}).execute()
    return response.data

@router.post("/invite")
async def invite_user(team_id: str, invited_user_id: str,user_id : str, session: SessionDep) -> TeamsUser:
    """
        Kullanıcıyı takıma davet eder
    """
    if user_id == invited_user_id:
        raise Exception("Kendi kendini takıma ekleyemezsiniz")
    user = await session.table("users").select("*").eq("id", user_id).execute()
    # user_id ile sessiondaki kullanıcıyı kontrol etmeliyim aynı kullanıcı mı diye
    if user_id != user.data[0].get("id"):
        raise Exception("Kullanıcı yetkisi yok")

    response = await session.rpc('invite_user', {'team_id': team_id, 'invited_user_id': invited_user_id,"user_id":user_id}).execute()
    return response.model_dump()

@router.post("/accept-invite")
async def accept_invite(team_id: str, user_id : str, session: SessionDep) -> TeamsUser:
    """
        Takım davetini kabul eder
    """
    response = await session.rpc('accept_invite', {'team_id': team_id, 'user_id': user_id}).execute()
    return response.model_dump()

@router.post("/reject-invite")
async def reject_invite(team_id: str, user_id : str, session: SessionDep) -> TeamsUser:
    """
        Takım davetini reddeder
    """
    response = await session.rpc('reject_invite', {'team_id': team_id, 'user_id': user_id}).execute()
    return response.model_dump()


@router.get("/create")
async def create_teams_user(teams_user_in: TeamsUserCreate, session: SessionDep) -> TeamsUser:
    return await teams_user.create(session, obj_in=teams_user_in)


@router.get("/read-all")
async def read_teams_users(session: SessionDep) -> list[TeamsUser]:
    return await teams_user.get_all(session)


# İlişkili tablodan geldiği için id ile veri çekmek mümkün değil
@router.get("/get-by-id/{id}",deprecated=True)
async def read_teams_user_by_id(id: str, session: SessionDep) -> TeamsUser | None:
    return await teams_user.get(session, id=id)

@router.get("/get-by-team/{team_id}")
async def read_teams_user_by_team(team_id: str, session: SessionDep) -> dict:
    """
        Takımdaki kullanıcıları getirir
    """
    result = {
        "teams_user": [],
        "users": [],
        "team" : None
    }
    teams_user_: list[TeamsUser] = await teams_user.get_multi_by_team(session, team_id=team_id)
    result["teams_user"] = teams_user_
    user_ids = [item.user_id for item in teams_user_]

    response = await session.rpc('get_users_by_team', {'team_id': team_id}).execute()

    result["users"] = response.data

    team = await session.table("teams").select("*").eq("id", team_id).execute()
    _, got = team
    result["team"] = team.data[0]
    return  result

@router.put("/update")
async def update_teams_user(teams_user_in: TeamsUserInDB, session: SessionDep) -> TeamsUser:
    """
        Kullanıcının rolünü günceller
    """
    return await teams_user.update(session, obj_in=teams_user_in)

@router.delete("/delete/{team_id}/{user_id}")
async def delete_teams_user(team_id: str, user_id: str, session: SessionDep) -> TeamsUser:
    """
        Kullanıcıyı takımdan çıkarır
    """
    response = await session.table("teams_user").delete().eq("team_id", team_id).eq("user_id", user_id).execute()
    return response

@router.get("/get-by-user/{user_id}")
async def read_teams_user_by_user(user_id: str, session: SessionDep) -> list[TeamsUser]:
    """
        Kullanıcının takımlarını getirir
    """
    return await teams_user.get_multi_by_user(session, user_id=user_id)

