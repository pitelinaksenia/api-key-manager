from uuid import UUID

from fastapi import HTTPException

from app.core.security import generate_api_key
from app.models.api_key import APIKey
from app.repositories.apikey_repository import APIKeyRepository
from app.schemas.apikey import APIKeyCreate, APIKeyCreateResponse
from app.services.client_service import ClientService
from app.services.scope_service import ScopeService


class APIKeyService:
    def __init__(
        self,
        apikey_repo: APIKeyRepository,
        scope_service: ScopeService,
        client_service: ClientService,
    ):
        self.apikey_repo = apikey_repo
        self.scope_service = scope_service
        self.client_service = client_service

    def create_api_key(
        self, client_id: UUID, apikey_data: APIKeyCreate
    ) -> APIKeyCreateResponse:
        client = self.client_service.get(client_id)
        if not client.is_active:
            raise HTTPException(status_code=400, detail="Client is not active")

        scopes = self.scope_service.get_by_codes(apikey_data.scope_codes)

        raw_k, prefix, k_hash = generate_api_key()
        api_key = APIKey(
            client_id=client_id,
            key_hash=k_hash,
            key_prefix=prefix,
            name=apikey_data.name,
            scopes=scopes,
            expires_at=apikey_data.expires_at,
        )

        result = self.apikey_repo.create(api_key)

        return APIKeyCreateResponse(
            id=result.id,
            name=result.name,
            key_prefix=result.key_prefix,
            status=result.status,
            scopes=[s.code for s in result.scopes],
            expires_at=result.expires_at,
            created_at=result.created_at,
            last_used_at=result.last_used_at,
            raw_key=raw_k,
        )

    def get_by_id(self, client_id: UUID) -> APIKey | None:
        pass

    def get_by_hash(self, key_hash: str) -> APIKey | None:
        pass

    def list_by_client(self, client_id: UUID) -> list[APIKey]:
        pass

    def update(self, api_key: APIKey) -> APIKey:
        pass
