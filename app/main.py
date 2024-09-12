import base64
import binascii
from typing import Annotated
from fastapi import  Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from supabase_py_async import AsyncClient
import uvicorn
from app.api.database import init_super_client
# from app.core.config import Settings
from app.core.events import exception_handler, lifespan
from jwt import ExpiredSignatureError, InvalidTokenError
from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.core.middleware import SupabaseAuthMiddleware

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)

from app.api.database import super_client

def create_app() -> FastAPI:


    # init FastAPI with lifespan
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=lambda router: f"{router.tags[0]}-{router.name}",
    )

    
    
    # set CORS
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def add_authentication(request: Request, call_next):
        
        supabase  = super_client or await init_super_client()
        if request.method == "OPTIONS" or request.url.path in ["/docs",'/api/v1/openapi.json','/api/v1/login/token']:
            return await call_next(request)
        body = await request.body()

        token = request.headers.get("authorization", "").replace("Bearer ", "")

        if not token:
            return Response("Unauthorized", status_code=401)

        try:
            auth = await supabase.auth.get_user(token)
            request.state.user = auth.user
            supabase.postgrest.auth(token)



        except Exception as e:
            return Response("Invalid user token" + str(e), status_code=401)

        return await call_next(request)


    
    # Include the routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()








if __name__ == "__main__":
    host = "localhost"
    port = 8000
    uvicorn.run(app, host=host, port=port)
