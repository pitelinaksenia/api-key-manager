from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService


def get_client_repository(session: Session = Depends(get_db)) -> ClientRepository:
    return ClientRepository(session)


def get_client_service(
    client_repo: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    return ClientService(client_repo)
