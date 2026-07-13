from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import ScopeAlreadyExistsError, ScopeNotFoundError
from app.schemas.scope import ScopeCreate
from app.services.scope_service import ScopeService


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return ScopeService(scope_repo=mock_repo)


async def test_get_returns_scope_when_found(service, mock_repo, scope_factory):
    scope_id = uuid4()
    expected_scope = scope_factory()
    mock_repo.get_by_id.return_value = expected_scope

    result = await service.get(scope_id)

    assert result is expected_scope
    mock_repo.get_by_id.assert_awaited_once_with(scope_id)


async def test_get_raises_not_found_when_missing(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    scope_id = uuid4()

    with pytest.raises(ScopeNotFoundError):
        await service.get(scope_id)


async def test_get_by_codes_returns_all_when_all_found(
    service, mock_repo, scope_factory
):
    scopes = [
        scope_factory(code="read", description="d"),
        scope_factory(code="write", description="d"),
    ]
    mock_repo.get_by_codes.return_value = scopes

    result = await service.get_by_codes(["read", "write"])

    assert result == scopes
    mock_repo.get_by_codes.assert_awaited_once_with(["read", "write"])


async def test_get_by_codes_raises_not_found_when_some_missing(
    service, mock_repo, scope_factory
):
    mock_repo.get_by_codes.return_value = [
        scope_factory(),
    ]

    with pytest.raises(ScopeNotFoundError):
        await service.get_by_codes(["read", "nonexistent"])


async def test_get_all_returns_all_scopes(service, mock_repo, scope_factory):
    scopes = [
        scope_factory(code="read"),
        scope_factory(code="write"),
    ]
    mock_repo.get_all.return_value = scopes

    result = await service.get_all()

    assert result == scopes
    mock_repo.get_all.assert_awaited_once()


async def test_create_returns_scope_on_success(service, mock_repo, scope_factory):
    scope_data = ScopeCreate(code="read", description="Read access")
    created_scope = scope_factory(code="read", description="Read access")
    mock_repo.create.return_value = created_scope

    result = await service.create(scope_data)

    assert result is created_scope
    mock_repo.create.assert_awaited_once_with(scope_data)


async def test_create_raises_already_exists_on_integrity_error(
    service, mock_repo, integrity_error
):
    scope_data = ScopeCreate(code="read", description="Read access")
    mock_repo.create.side_effect = integrity_error
    mock_repo.session = AsyncMock()

    with pytest.raises(ScopeAlreadyExistsError):
        await service.create(scope_data)

    mock_repo.session.rollback.assert_awaited_once()
