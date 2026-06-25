from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr


class ClientResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    is_active: bool | None = None
    name: str | None = None
