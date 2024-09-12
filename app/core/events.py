"""
life span events
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.database import init_connection, init_super_client
from app.core.middleware import SupabaseAuthMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """life span events"""
    try:
        await init_super_client()

        
        # await init_connection()
        logging.info("lifespan start")
        yield
    finally:
        logging.info("lifespan shutdown")



async def exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
