from multiprocessing.dummy.connection import Client
from uuid import UUID

from fastapi import HTTPException

from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def register(self, client_data: ClientCreate) -> Client:
        return await self.client_repo.create(client_data)

    async def get(self, client_id: UUID) -> Client:
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    async def get_all(self) -> list[Client]:
        return await self.client_repo.get_all()

    async def update(self, client_id: UUID, client_data: ClientUpdate) -> Client:
        client = await self.get(client_id)
        return await self.client_repo.update(client, client_data)
