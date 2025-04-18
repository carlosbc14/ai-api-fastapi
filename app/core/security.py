from fastapi import HTTPException, Header
from app.core.config import settings


def api_key_auth(api_key: str = Header(..., alias="X-API-Key")):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
