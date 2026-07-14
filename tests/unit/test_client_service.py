from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions.exceptions import ClientAlreadyExistsError, ClientNotFoundError
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client_service import ClientService


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return ClientService(client_repo=mock_repo)


async def test_get_returns_client_when_found(service, mock_repo, client_factory):
    client_id = uuid4()
    expected_client = client_factory()
    mock_repo.get_by_id.return_value = expected_client

    result = await service.get(client_id)

    assert result is expected_client
    mock_repo.get_by_id.assert_awaited_once_with(client_id)


async def test_get_raises_not_found_when_missing(service, mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ClientNotFoundError):
        await service.get(uuid4())


async def test_get_all_returns_all_clients(service, mock_repo, client_factory):
    clients = [
        client_factory(name="A", email="a@a.com"),
        client_factory(name="B", email="b@b.com"),
    ]
    mock_repo.get_all.return_value = clients

    result = await service.get_all()

    assert result == clients
    mock_repo.get_all.assert_awaited_once()


async def test_register_returns_client_on_success(service, mock_repo, client_factory):
    client_data = ClientCreate(name="Acme", email="a@acme.com")
    created_client = client_factory(name="Acme", email="a@acme.com")
    mock_repo.create.return_value = created_client

    result = await service.register(client_data)

    assert result is created_client
    mock_repo.create.assert_awaited_once_with(client_data)


async def test_register_raises_already_exists_on_integrity_error(
    service, mock_repo, integrity_error
):
    client_data = ClientCreate(name="Acme", email="a@acme.com")
    mock_repo.create.side_effect = integrity_error
    mock_repo.session = AsyncMock()

    with pytest.raises(ClientAlreadyExistsError):
        await service.register(client_data)

    mock_repo.session.rollback.assert_awaited_once()


async def test_update_raises_not_found_when_client_missing(service, mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ClientNotFoundError):
        await service.update(uuid4(), ClientUpdate(name=None, is_active=None))

    mock_repo.update.assert_not_awaited()


async def test_update_with_empty_payload_calls_repo_and_returns_client(
    service, mock_repo, client_factory
):
    existing_client = client_factory()
    mock_repo.get_by_id.return_value = existing_client
    mock_repo.update.return_value = existing_client

    result = await service.update(
        existing_client.id, ClientUpdate(name=None, is_active=None)
    )

    mock_repo.get_by_id.assert_awaited_once_with(existing_client.id)
    mock_repo.update.assert_awaited_once_with(
        existing_client, ClientUpdate(name=None, is_active=None)
    )
    assert result is existing_client
