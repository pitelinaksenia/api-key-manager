from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scope import Scope
from app.schemas.scope import ScopeCreate


class ScopeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, scope_id: UUID) -> Scope | None:
        return await self.session.get(Scope, scope_id)

    async def get_all(self) -> list[Scope]:
        stmt = select(Scope)
        return list(await self.session.scalars(stmt))

    async def get_by_codes(self, codes: list[str]) -> list[Scope]:
        stmt = select(Scope).where(Scope.code.in_(codes))
        return list(await self.session.scalars(stmt))

    async def create(self, scope_data: ScopeCreate) -> Scope:
        scope = Scope(code=scope_data.code, description=scope_data.description)
        self.session.add(scope)
        await self.session.commit()
        await self.session.refresh(scope)
        return scope
