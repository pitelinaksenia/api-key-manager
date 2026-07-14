from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.core.exceptions.exceptions import (
    APIKeyAlreadyRevokedError,
    APIKeyInvalidError,
    APIKeyNotFoundError,
    ClientNotActiveError,
)
from app.models.enums import APIKeyStatus
from app.schemas.apikey import APIKeyCreate
from app.services.apikey_service import APIKeyService


@pytest.fixture
def mock_apikey_repo():
    return AsyncMock()


@pytest.fixture
def mock_scope_service():
    return AsyncMock()


@pytest.fixture
def mock_client_service():
    return AsyncMock()


@pytest.fixture
def service(mock_apikey_repo, mock_scope_service, mock_client_service):
    return APIKeyService(
        apikey_repo=mock_apikey_repo,
        scope_service=mock_scope_service,
        client_service=mock_client_service,
    )


# --- create_api_key ---


async def test_create_api_key_raises_when_client_not_active(
    service, mock_client_service, client_factory
):
    client_id = uuid4()
    inactive_client = client_factory(id=client_id, is_active=False)
    mock_client_service.get.return_value = inactive_client

    with pytest.raises(ClientNotActiveError):
        await service.create_api_key(
            client_id, APIKeyCreate(name="key", scope_codes=["read"], expires_at=None)
        )


async def test_create_api_key_success(
    service,
    mock_client_service,
    mock_scope_service,
    mock_apikey_repo,
    client_factory,
    scope_factory,
    api_key_factory,
):
    client_id = uuid4()
    active_client = client_factory(id=client_id)
    mock_client_service.get.return_value = active_client

    scopes = [scope_factory()]
    mock_scope_service.get_by_codes.return_value = scopes

    created_key = api_key_factory(client_id=client_id, scopes=scopes)
    mock_apikey_repo.create.return_value = created_key

    with patch(
        "app.services.apikey_service.generate_api_key",
        return_value=("raw_key_123", "pfx", "hash"),
    ):
        result = await service.create_api_key(
            client_id,
            APIKeyCreate(name="key", scope_codes=["read"], expires_at=None),
        )

    assert result.raw_key == "raw_key_123"
    assert result.scopes == ["read"]
    assert result.id == created_key.id
    mock_scope_service.get_by_codes.assert_awaited_once_with(["read"])
    mock_apikey_repo.create.assert_awaited_once()


# --- get ---


async def test_get_returns_api_key_when_found(
    service, mock_apikey_repo, api_key_factory
):
    key_id = uuid4()
    expected_key = api_key_factory(id=key_id)
    mock_apikey_repo.get_by_id.return_value = expected_key

    result = await service.get(key_id)

    assert result is expected_key
    mock_apikey_repo.get_by_id.assert_awaited_once_with(key_id)


async def test_get_raises_not_found_when_missing(service, mock_apikey_repo):
    mock_apikey_repo.get_by_id.return_value = None

    with pytest.raises(APIKeyNotFoundError):
        await service.get(uuid4())


# --- get_by_client ---


async def test_get_by_client_returns_key_when_matches(
    service, mock_apikey_repo, api_key_factory
):
    client_id = uuid4()
    key_id = uuid4()
    matching_key = api_key_factory(id=key_id, client_id=client_id)
    mock_apikey_repo.get_by_id.return_value = matching_key

    result = await service.get_by_client(client_id, key_id)

    assert result is matching_key


async def test_get_by_client_raises_not_found_when_client_mismatch(
    service, mock_apikey_repo, api_key_factory
):
    key_id = uuid4()
    other_client_id = uuid4()
    key_belongs_to_someone_else = api_key_factory(id=key_id, client_id=other_client_id)
    mock_apikey_repo.get_by_id.return_value = key_belongs_to_someone_else

    with pytest.raises(APIKeyNotFoundError):
        await service.get_by_client(uuid4(), key_id)


# --- list_by_client ---


async def test_list_by_client_calls_client_service_and_returns_keys(
    service, mock_client_service, mock_apikey_repo, scope_factory, api_key_factory
):
    client_id = uuid4()
    scopes = [scope_factory(code="read")]
    keys = [api_key_factory(client_id=client_id, scopes=scopes)]
    mock_apikey_repo.list_by_client.return_value = keys

    result = await service.list_by_client(client_id)

    assert len(result) == 1
    assert result[0].id == keys[0].id
    assert result[0].scopes == ["read"]
    mock_client_service.get.assert_awaited_once_with(client_id)
    mock_apikey_repo.list_by_client.assert_awaited_once_with(client_id)


# --- verify_api_key ---


async def test_verify_api_key_raises_invalid_when_not_found(service, mock_apikey_repo):
    mock_apikey_repo.get_by_hash.return_value = None

    with patch("app.services.apikey_service.hash_key", return_value="hashed"):
        with pytest.raises(APIKeyInvalidError):
            await service.verify_api_key("raw_key")


async def test_verify_api_key_raises_invalid_when_not_active(
    service, mock_apikey_repo, api_key_factory
):
    inactive_key = api_key_factory(
        status=APIKeyStatus.REVOKED,
        expires_at=None,
    )
    mock_apikey_repo.get_by_hash.return_value = inactive_key

    with patch("app.services.apikey_service.hash_key", return_value="hashed"):
        with pytest.raises(APIKeyInvalidError):
            await service.verify_api_key("raw_key")


async def test_verify_api_key_raises_invalid_when_expired(
    service, mock_apikey_repo, api_key_factory
):
    expired_key = api_key_factory(
        status=APIKeyStatus.ACTIVE,
        expires_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    mock_apikey_repo.get_by_hash.return_value = expired_key

    with patch("app.services.apikey_service.hash_key", return_value="hashed"):
        with pytest.raises(APIKeyInvalidError):
            await service.verify_api_key("raw_key")


async def test_verify_api_key_success_updates_last_used_and_returns_response(
    service, mock_apikey_repo, scope_factory, api_key_factory
):
    scopes = [scope_factory()]
    client_id = uuid4()
    valid_key = api_key_factory(
        client_id=client_id,
        status=APIKeyStatus.ACTIVE,
        expires_at=None,
        scopes=scopes,
        last_used_at=None,
    )
    mock_apikey_repo.get_by_hash.return_value = valid_key

    with patch("app.services.apikey_service.hash_key", return_value="hashed"):
        result = await service.verify_api_key("raw_key")

    assert result.client_id == client_id
    assert result.scopes == ["read"]
    assert valid_key.last_used_at is not None
    mock_apikey_repo.update.assert_awaited_once_with(valid_key)


# --- revoke_api_key ---


async def test_revoke_api_key_raises_when_already_revoked(
    service, mock_apikey_repo, api_key_factory
):
    key_id = uuid4()
    already_revoked = api_key_factory(
        id=key_id,
        status=APIKeyStatus.REVOKED,
    )
    mock_apikey_repo.get_by_id.return_value = already_revoked

    with pytest.raises(APIKeyAlreadyRevokedError):
        await service.revoke_api_key(key_id)

    mock_apikey_repo.update.assert_not_awaited()


async def test_revoke_api_key_success(service, mock_apikey_repo, api_key_factory):
    key_id = uuid4()
    active_key = api_key_factory(
        id=key_id,
        status=APIKeyStatus.ACTIVE,
    )
    mock_apikey_repo.get_by_id.return_value = active_key

    result = await service.revoke_api_key(key_id)

    assert result.status == APIKeyStatus.REVOKED
    assert active_key.revoked_at is not None
    mock_apikey_repo.update.assert_awaited_once_with(active_key)
