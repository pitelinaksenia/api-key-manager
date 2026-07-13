from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.api_key import APIKey
from app.models.client import Client
from app.models.enums import APIKeyStatus
from app.models.scope import Scope


def make_client(
    *,
    id: UUID | None = None,
    name: str = "Acme",
    email: str = "a@acme.com",
    is_active: bool = True,
) -> Client:
    return Client(
        id=id or uuid4(),
        name=name,
        email=email,
        is_active=is_active,
    )


def make_scope(
    *,
    id: UUID | None = None,
    code: str = "read",
    description: str = "d",
) -> Scope:
    return Scope(id=id or uuid4(), code=code, description=description, api_keys=[])


def make_api_key(
    *,
    id: UUID | None = None,
    client_id: UUID | None = None,
    key_hash: str = "hash",
    key_prefix: str = "pfx",
    name: str = "key",
    scopes: list[Scope] | None = None,
    status: APIKeyStatus = APIKeyStatus.ACTIVE,
    expires_at: datetime | None = None,
    last_used_at: datetime | None = None,
    revoked_at: datetime | None = None,
) -> APIKey:
    return APIKey(
        id=id or uuid4(),
        client_id=client_id or uuid4(),
        key_hash=key_hash,
        key_prefix=key_prefix,
        name=name,
        scopes=scopes or [],
        status=status,
        expires_at=expires_at,
        last_used_at=last_used_at,
        revoked_at=revoked_at,
        created_at=datetime.now(timezone.utc),
    )


def make_integrity_error() -> IntegrityError:
    return IntegrityError("stmt", "params", Exception("duplicate key"))


@pytest.fixture
def client_factory():
    return make_client


@pytest.fixture
def scope_factory():
    return make_scope


@pytest.fixture
def api_key_factory():
    return make_api_key


@pytest.fixture
def integrity_error():
    return make_integrity_error()
