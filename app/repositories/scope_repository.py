from uuid import UUID

from sqlalchemy.orm import Session

from app.models.scope import Scope
from app.schemas.scope import ScopeCreate


class ScopeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, scope_id: UUID) -> Scope | None:
        return self.session.get(Scope, scope_id)

    def get_all(self) -> list[Scope]:
        return self.session.query(Scope).all()

    def create(self, scope_data: ScopeCreate) -> Scope:
        scope = Scope(code=scope_data.code, description=scope_data.description)
        self.session.add(scope)
        self.session.commit()
        self.refresh(scope)
        return scope
