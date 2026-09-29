import os

from fastapi import Header, HTTPException


def require_auth(
    user_id: str | None = Header(default=None, alias="user_id"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> str:
    if not user_id or not authorization:
        raise HTTPException(
            status_code=400,
            detail="Missing required headers: user_id and Authorization",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must use Bearer scheme",
        )

    api_key = authorization.removeprefix("Bearer ")
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user_id
