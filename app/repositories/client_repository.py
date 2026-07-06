from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, client_data: ClientCreate) -> Client:
        client = Client(name=client_data.name, email=client_data.email)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_all(self) -> list[Client]:
        stmt = select(Client)
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_by_id(self, client_id: UUID) -> Client | None:
        return await self.session.get(Client, client_id)

    async def update(self, client: Client, client_data: ClientUpdate) -> Client:
        if client_data.is_active is not None:
            client.is_active = client_data.is_active

        if client_data.name is not None:
            client.name = client_data.name

        await self.session.commit()
        await self.session.refresh(client)
        return client
