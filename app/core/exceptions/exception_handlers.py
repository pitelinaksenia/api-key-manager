from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.exceptions import (
    AlreadyExistsError,
    AuthenticationError,
    AuthorizationError,
    InvalidStateError,
    NotFoundError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        logger.warning(
            "not_found",
            detail=str(exc),
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        logger.warning(
            "already_exists",
            detail=str(exc),
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidStateError)
    async def invalid_state_handler(request: Request, exc: InvalidStateError):
        logger.warning(
            "invalid_state",
            detail=str(exc),
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, exc: AuthenticationError):
        logger.warning(
            "authentication_failed",
            detail=str(exc),
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(request: Request, exc: AuthorizationError):
        logger.warning(
            "authorization_failed",
            detail=str(exc),
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(
            "unhandled_exception",
            error=str(exc),
            error_type=type(exc).__name__,
            path=request.url.path,
            method=request.method,
            exc_info=True,
        )
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
