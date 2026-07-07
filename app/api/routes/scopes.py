from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_scope_service
from app.schemas.scope import ScopeCreate, ScopeResponse
from app.services.scope_service import ScopeService

router = APIRouter(
    prefix="/scopes",
    tags=["scopes"],
)


@router.post("/", response_model=ScopeResponse, status_code=201)
async def create_scope(
    scope_data: ScopeCreate,
    scope_service: ScopeService = Depends(get_scope_service),
) -> ScopeResponse:
    return await scope_service.create(scope_data)


@router.get("/", response_model=list[ScopeResponse])
async def get_scopes(
    scope_service: ScopeService = Depends(get_scope_service),
) -> list[ScopeResponse]:
    return await scope_service.get_all()


@router.get("/{scope_id}", response_model=ScopeResponse)
async def get_scope_by_id(
    scope_id: UUID, scope_service: ScopeService = Depends(get_scope_service)
) -> ScopeResponse:
    return await scope_service.get(scope_id)
