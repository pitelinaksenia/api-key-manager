from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.api_key import APIKey


class APIKeyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, api_key: APIKey) -> APIKey:
        self.session.add(api_key)
        self.session.commit()
        self.session.refresh(api_key)
        return api_key

    def get_by_id(self, key_id: UUID) -> APIKey | None:
        stmt = (
            select(APIKey)
            .where(APIKey.id == key_id)
            .options(selectinload(APIKey.scopes))
        )
        return self.session.scalars(stmt).first()

    def get_by_hash(self, key_hash: str) -> APIKey | None:
        stmt = (
            select(APIKey)
            .where(APIKey.key_hash == key_hash)
            .options(selectinload(APIKey.scopes))
        )
        return self.session.scalars(stmt).first()

    def list_by_client(self, client_id: UUID) -> list[APIKey]:
        stmt = (
            select(APIKey)
            .where(APIKey.client_id == client_id)
            .options(selectinload(APIKey.scopes))
        )
        return list(self.session.scalars(stmt))

    def update(self, api_key: APIKey) -> APIKey:
        self.session.commit()
        self.session.refresh(api_key)
        return api_key
