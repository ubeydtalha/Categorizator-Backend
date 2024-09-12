from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login , category, favorite , team , teams_user
from app.api.api_v1.websockets import sync_ws_router
api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(favorite.router, prefix="/favorite", tags=["favorite"])
api_router.include_router(team.router, prefix="/team", tags=["team"])
api_router.include_router(teams_user.router, prefix="/teams-user", tags=["teams_user"])
api_router.include_router(sync_ws_router, prefix="/sync", tags=["ws"])