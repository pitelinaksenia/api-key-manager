from uuid import UUID

from fastapi import HTTPException

from app.models.scope import Scope
from app.repositories.scope_repository import ScopeRepository
from app.schemas.scope import ScopeCreate


class ScopeService:
    def __init__(self, scope_repo: ScopeRepository):
        self.scope_repo = scope_repo

    async def get(self, scope_id: UUID) -> Scope:
        scope = await self.scope_repo.get_by_id(scope_id)
        if not scope:
            raise HTTPException(status_code=404, detail="Scope not found")
        return scope

    async def get_by_codes(self, codes: list[str]) -> list[Scope]:
        scopes = await self.scope_repo.get_by_codes(codes)
        if len(scopes) != len(codes):
            raise HTTPException(status_code=404, detail="One or more scopes not found")
        return scopes

    async def get_all(self) -> list[Scope]:
        return await self.scope_repo.get_all()

    async def create(self, scope_data: ScopeCreate) -> Scope:
        return await self.scope_repo.create(scope_data)
