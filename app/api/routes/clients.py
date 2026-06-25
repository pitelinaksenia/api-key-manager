from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_client_service
from app.models import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(
    client_data: ClientCreate,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    return client_service.register(client_data)


@router.get("/", response_model=list[ClientResponse])
async def get_clients(
    client_service: ClientService = Depends(get_client_service),
) -> list[ClientResponse]:
    return client_service.get_all()


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(
    client_id: UUID, client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    return client_service.get(client_id)


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: UUID,
    client_data: ClientUpdate,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    return client_service.update(client_id, client_data)
