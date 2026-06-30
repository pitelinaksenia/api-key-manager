from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import APIKeyStatus


class APIKeyCreate(BaseModel):
    name: str
    scope_codes: list[str]
    expires_at: datetime | None = None


class APIKeyResponse(BaseModel):
    id: UUID
    name: str
    key_prefix: str
    status: APIKeyStatus
    scopes: list[str]
    expires_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None

    class Config:
        from_attributes = True


class APIKeyCreateResponse(APIKeyResponse):
    raw_key: str
