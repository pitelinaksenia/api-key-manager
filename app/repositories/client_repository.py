from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, client_data: ClientCreate) -> Client:
        client = Client(name=client_data.name, email=client_data.email)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_all(self) -> list[Client]:
        return self.session.query(Client).all()

    def get_by_id(self, client_id: UUID) -> Client | None:
        return self.session.get(Client, client_id)

    def update(self, client: Client, client_data: ClientUpdate) -> Client:
        if client_data.is_active is not None:
            client.is_active = client_data.is_active

        if client_data.name is not None:
            client.name = client_data.name

        self.session.commit()
        self.session.refresh(client)

        return client
