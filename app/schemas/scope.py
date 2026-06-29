from uuid import UUID

from pydantic import BaseModel


class ScopeCreate(BaseModel):
    code: str
    description: str


class ScopeResponse(BaseModel):
    id: UUID
    code: str
    description: str | None
    api_keys: list[str] | None
