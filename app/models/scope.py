import uuid
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scope(Base):
    __tablename__ = "scopes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    api_keys: Mapped[list["APIKey"]] = relationship(
        secondary="api_key_scopes",
        back_populates="scopes",
    )


api_key_scopes = Table(
    "api_key_scopes",
    Base.metadata,
    Column("api_key_id", ForeignKey("api_keys.id"), primary_key=True),
    Column("scope_id", ForeignKey("scopes.id"), primary_key=True),
)
