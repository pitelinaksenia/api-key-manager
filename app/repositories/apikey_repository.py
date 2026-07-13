from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import APIKey


class APIKeyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, api_key: APIKey) -> APIKey:
        self.session.add(api_key)
        await self.session.commit()
        await self.session.refresh(api_key)
        return api_key

    async def get_by_id(self, key_id: UUID) -> APIKey | None:
        stmt = select(APIKey).where(APIKey.id == key_id).options(APIKey.scopes)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_hash(self, key_hash: str) -> APIKey | None:
        stmt = select(APIKey).where(APIKey.key_hash == key_hash).options(APIKey.scopes)
        result = await self.session.scalars(stmt)
        return result.first()

    async def list_by_client(self, client_id: UUID) -> list[APIKey]:
        stmt = (
            select(APIKey).where(APIKey.client_id == client_id).options(APIKey.scopes)
        )
        return list(await self.session.scalars(stmt))

    async def update(self, api_key: APIKey) -> APIKey:
        await self.session.commit()
        await self.session.refresh(api_key)
        return api_key
