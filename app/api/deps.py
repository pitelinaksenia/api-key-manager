from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.apikey_repository import APIKeyRepository
from app.repositories.client_repository import ClientRepository
from app.repositories.scope_repository import ScopeRepository
from app.services.apikey_service import APIKeyService
from app.services.client_service import ClientService
from app.services.scope_service import ScopeService


def get_client_repository(session: Session = Depends(get_db)) -> ClientRepository:
    return ClientRepository(session)


def get_client_service(
    client_repo: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    return ClientService(client_repo)


def get_apikey_repository(session: Session = Depends(get_db)) -> APIKeyRepository:
    return APIKeyRepository(session)


def get_apikey_service(
    apikey_repo: APIKeyRepository = Depends(get_apikey_repository),
) -> APIKeyService:
    return APIKeyService(apikey_repo)


def get_scope_repository(session: Session = Depends(get_db)) -> ScopeRepository:
    return ScopeRepository(session)


def get_scope_service(
    scope_repo: ScopeRepository = Depends(get_scope_repository),
) -> APIKeyService:
    return ScopeService(scope_repo)
