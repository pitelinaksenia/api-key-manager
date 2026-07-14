from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.exceptions import APIKeyInvalidError, InsufficientScopeError
from app.database import get_db
from app.repositories.apikey_repository import APIKeyRepository
from app.repositories.client_repository import ClientRepository
from app.repositories.scope_repository import ScopeRepository
from app.services.apikey_service import APIKeyService
from app.services.client_service import ClientService
from app.services.scope_service import ScopeService


def get_client_repository(
    session: AsyncSession = Depends(get_db),
) -> ClientRepository:
    return ClientRepository(session)


def get_client_service(
    client_repo: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    return ClientService(client_repo)


def get_scope_repository(
    session: AsyncSession = Depends(get_db),
) -> ScopeRepository:
    return ScopeRepository(session)


def get_scope_service(
    scope_repo: ScopeRepository = Depends(get_scope_repository),
) -> APIKeyService:
    return ScopeService(scope_repo)


def get_apikey_repository(
    session: AsyncSession = Depends(get_db),
) -> APIKeyRepository:
    return APIKeyRepository(session)


def get_apikey_service(
    apikey_repo: APIKeyRepository = Depends(get_apikey_repository),
    scope_service: ScopeService = Depends(get_scope_service),
    client_service: ClientService = Depends(get_client_service),
) -> APIKeyService:
    return APIKeyService(apikey_repo, scope_service, client_service)


async def get_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    apikey_service: APIKeyService = Depends(get_apikey_service),
):
    return await apikey_service.verify_api_key(x_api_key)


def require_scope(scope: str):
    async def _check(api_key=Depends(get_api_key)):
        if scope not in api_key.scopes:
            raise InsufficientScopeError(scope)
        return api_key

    return _check
