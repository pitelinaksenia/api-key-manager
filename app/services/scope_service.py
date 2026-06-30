from uuid import UUID

from fastapi import HTTPException

from app.models.scope import Scope
from app.repositories.scope_repository import ScopeRepository
from app.schemas.scope import ScopeCreate


class ScopeService:
    def __init__(self, scope_repo: ScopeRepository):
        self.scope_repo = scope_repo

    def get(self, scope_id: UUID) -> Scope:
        scope = self.scope_repo.get()
        if not scope:
            raise HTTPException(status_code=404, detail="Scope not found")
        return scope

    def get_by_codes(self, codes: list[str]) -> list[Scope]:
        scopes = self.scope_repo.get_by_codes(codes)
        if len(scopes) != len(codes):
            raise HTTPException(status_code=404, detail="One or more scopes not found")
        return scopes

    def get_all(self) -> list[Scope]:
        return self.scope_repo.get_all()

    def create(self, scope_data: ScopeCreate) -> Scope:
        return self.scope_repo.create()
