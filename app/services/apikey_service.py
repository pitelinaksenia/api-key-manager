from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import (
    APIKeyAlreadyRevokedError,
    APIKeyInvalidError,
    APIKeyNotFoundError,
    ClientNotActiveError,
)
from app.core.security import generate_api_key, hash_key
from app.models.api_key import APIKey
from app.models.enums import APIKeyStatus
from app.repositories.apikey_repository import APIKeyRepository
from app.schemas.apikey import (
    APIKeyCreate,
    APIKeyCreateResponse,
    APIKeyResponse,
    APIKeyRevokeResponse,
    APIKeyVerifyResponse,
)
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

    def _to_response(self, api_key: APIKey) -> APIKeyResponse:
        return APIKeyResponse(
            id=api_key.id,
            name=api_key.name,
            key_prefix=api_key.key_prefix,
            status=api_key.status,
            scopes=[s.code for s in api_key.scopes],
            expires_at=api_key.expires_at,
            created_at=api_key.created_at,
            last_used_at=api_key.last_used_at,
        )

    async def create_api_key(
        self, client_id: UUID, apikey_data: APIKeyCreate
    ) -> APIKeyCreateResponse:
        client = await self.client_service.get(client_id)
        if not client.is_active:
            raise ClientNotActiveError(client_id)

        scopes = await self.scope_service.get_by_codes(apikey_data.scope_codes)

        raw_k, prefix, k_hash = generate_api_key()
        api_key = APIKey(
            client_id=client_id,
            key_hash=k_hash,
            key_prefix=prefix,
            name=apikey_data.name,
            scopes=scopes,
            expires_at=apikey_data.expires_at,
        )

        result = await self.apikey_repo.create(api_key)

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

    async def get(self, key_id: UUID) -> APIKey:
        api_key = await self.apikey_repo.get_by_id(key_id)
        if not api_key:
            raise APIKeyNotFoundError(key_id)
        return api_key

    async def get_by_client(self, client_id: UUID, key_id: UUID) -> APIKey:
        api_key = await self.get(key_id)
        if api_key.client_id != client_id:
            raise APIKeyNotFoundError(key_id)
        return api_key

    async def list_by_client(self, client_id: UUID) -> list[APIKeyResponse]:
        await self.client_service.get(
            client_id
        )  # raises ClientNotFoundError if not found
        api_keys = await self.apikey_repo.list_by_client(client_id)
        return [self._to_response(key) for key in api_keys]

    async def verify_api_key(self, raw_key: str) -> APIKeyVerifyResponse:
        api_key_hash = hash_key(raw_key)
        api_key = await self.apikey_repo.get_by_hash(api_key_hash)

        if not api_key:
            raise APIKeyInvalidError()

        if api_key.status != APIKeyStatus.ACTIVE:
            raise APIKeyInvalidError()

        if api_key.expires_at and api_key.expires_at < datetime.now(timezone.utc):
            raise APIKeyInvalidError()

        api_key.last_used_at = datetime.now(timezone.utc)
        await self.apikey_repo.update(api_key)

        return APIKeyVerifyResponse(
            client_id=api_key.client_id,
            scopes=[s.code for s in api_key.scopes],
        )

    async def revoke_api_key(self, key_id: UUID) -> APIKeyRevokeResponse:
        api_key = await self.get(key_id)

        if api_key.status == APIKeyStatus.REVOKED:
            raise APIKeyAlreadyRevokedError(key_id)

        api_key.status = APIKeyStatus.REVOKED
        api_key.revoked_at = datetime.now(timezone.utc)
        await self.apikey_repo.update(api_key)
        return APIKeyRevokeResponse(
            id=api_key.id,
            status=api_key.status,
            revoked_at=api_key.revoked_at,
        )
