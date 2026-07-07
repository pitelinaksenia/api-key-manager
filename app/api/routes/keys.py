from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_apikey_service
from app.schemas.apikey import (
    APIKeyCreate,
    APIKeyCreateResponse,
    APIKeyResponse,
    APIKeyRevokeResponse,
    APIKeyVerifyRequest,
    APIKeyVerifyResponse,
)
from app.services.apikey_service import APIKeyService

router = APIRouter(tags=["api-keys"])


@router.post(
    "/clients/{client_id}/api-keys",
    response_model=APIKeyCreateResponse,
    status_code=201,
)
async def create_api_key(
    client_id: UUID,
    apikey_data: APIKeyCreate,
    apikey_service: APIKeyService = Depends(get_apikey_service),
):
    return await apikey_service.create_api_key(client_id, apikey_data)


@router.get("/clients/{client_id}/api-keys", response_model=list[APIKeyResponse])
async def get_client_list(
    client_id: UUID,
    apikey_service: APIKeyService = Depends(get_apikey_service),
) -> list[APIKeyResponse]:
    return await apikey_service.list_by_client(client_id)


@router.get("/clients/{client_id}/api-keys/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    client_id: UUID,
    key_id: UUID,
    apikey_service: APIKeyService = Depends(get_apikey_service),
):
    return await apikey_service.get_by_client(client_id, key_id)


@router.post("/api-keys/{key_id}/revoke", response_model=APIKeyRevokeResponse)
async def revoke_api_key(
    key_id: UUID,
    apikey_service: APIKeyService = Depends(get_apikey_service),
):
    return await apikey_service.revoke_api_key(key_id)


@router.post("/api-keys/verify", response_model=APIKeyVerifyResponse)
async def verify_api_key(
    verify_data: APIKeyVerifyRequest,
    apikey_service: APIKeyService = Depends(get_apikey_service),
):
    return await apikey_service.verify_api_key(verify_data.raw_key)
