from fastapi import APIRouter
from fastapi.params import Depends

from app.api.deps import require_scope
from app.api.routes.keys import get_api_key

router = APIRouter(
    prefix="/demo",
    tags=["demo"],
)


@router.get("/protected")
async def protected_demo(api_key=Depends(get_api_key)):
    return {
        "message": "Доступ разрешён — ключ валиден",
        "client_id": api_key.client_id,
        "scopes": api_key.scopes,
    }


@router.get("/admin-only")
async def admin_demo(api_key=Depends(require_scope("admin"))):
    return {
        "message": "Доступ разрешён — у ключа есть scope 'admin'",
        "client_id": api_key.client_id,
    }
