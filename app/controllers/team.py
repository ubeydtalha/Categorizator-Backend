
from ..main import supabase , app

from fastapi import APIRouter

router = APIRouter()

@router.get("/teams")
async def get_teams():
    teams = await supabase.table("teams").select("*").execute()
    return teams

@router.get("/teams/{team_id}")
async def get_team(team_id: int):
    team = await supabase.table("teams").select("*").eq("id", team_id).single().execute()
    return team

@router.post("/teams")
async def create_team(team: dict):
    new_team = await supabase.table("teams").insert(team).execute()
    return new_team

@router.put("/teams/{team_id}")
async def update_team(team_id: int, team: dict):
    updated_team = await supabase.table("teams").update(team).eq("id", team_id).execute()
    return updated_team

@router.delete("/teams/{team_id}")
async def delete_team(team_id: int):
    deleted_team = await supabase.table("teams").delete().eq("id", team_id).execute()
    return deleted_team