from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import APIKeyStatus


class APIKeyCreate(BaseModel):
    name: str
    scope_codes: list[str]
    expires_at: datetime | None = None


class APIKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    key_prefix: str
    status: APIKeyStatus
    scopes: list[str]
    expires_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None


class APIKeyCreateResponse(APIKeyResponse):
    raw_key: str


class APIKeyVerifyResponse(BaseModel):
    client_id: UUID
    scopes: list[str]


class APIKeyRevokeResponse(BaseModel):
    id: UUID
    status: APIKeyStatus
    revoked_at: datetime


class APIKeyVerifyRequest(BaseModel):
    raw_key: str
