from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scope import Scope
from app.schemas.scope import ScopeCreate


class ScopeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, scope_id: UUID) -> Scope | None:
        stmt = select(Scope).options(Scope.api_keys).where(Scope.id == scope_id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Scope]:
        stmt = select(Scope).options(Scope.api_keys)
        return list(await self.session.scalars(stmt))

    async def get_by_codes(self, codes: list[str]) -> list[Scope]:
        stmt = select(Scope).where(Scope.code.in_(codes))
        return list(await self.session.scalars(stmt))

    async def create(self, scope_data: ScopeCreate) -> Scope:
        scope = Scope(**scope_data.model_dump())
        self.session.add(scope)
        await self.session.commit()
        await self.session.refresh(scope, attribute_names=["api_keys"])
        return scope
