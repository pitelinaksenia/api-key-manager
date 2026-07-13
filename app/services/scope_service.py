from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ScopeAlreadyExistsError, ScopeNotFoundError
from app.models.scope import Scope
from app.repositories.scope_repository import ScopeRepository
from app.schemas.scope import ScopeCreate


class ScopeService:
    def __init__(self, scope_repo: ScopeRepository):
        self.scope_repo = scope_repo

    async def get(self, scope_id: UUID) -> Scope:
        scope = await self.scope_repo.get_by_id(scope_id)
        if not scope:
            raise ScopeNotFoundError(scope_id)
        return scope

    async def get_by_codes(self, codes: list[str]) -> list[Scope]:
        scopes = await self.scope_repo.get_by_codes(codes)
        if len(scopes) != len(codes):
            found_codes = {s.code for s in scopes}
            missing = set(codes) - found_codes
            raise ScopeNotFoundError(missing)
        return scopes

    async def get_all(self) -> list[Scope]:
        return await self.scope_repo.get_all()

    async def create(self, scope_data: ScopeCreate) -> Scope:
        try:
            return await self.scope_repo.create(scope_data)
        except IntegrityError:
            await self.scope_repo.session.rollback()
            raise ScopeAlreadyExistsError(scope_data.code)
