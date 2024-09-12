from typing import Optional
from fastapi import HTTPException, Request
from starlette.middleware.authentication import AuthenticationMiddleware

from supabase import client

from app.api.database import get_current_user

class SupabaseAuthMiddleware(AuthenticationMiddleware):
    async def authenticate(self, request: Request):
        auth_header: Optional[str] = request.headers.get("Authorization")
        if not auth_header:
            return None  # No Authorization header

        try:
            token = auth_header.split("Bearer ")[1]
        except IndexError:
            raise HTTPException(status_code=400, detail="Invalid token format")

        # Verify the token with Supabase
        user = await get_current_user(token)
        if user:
            return user, None  # Return user and None (indicating no custom auth data needed)
        else:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

