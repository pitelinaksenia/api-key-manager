from fastapi import FastAPI

from app.api.routes import clients, demo, keys, scopes
from app.core.config import Environment, settings
from app.core.exceptions.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging, get_logger

configure_logging(json_logs=settings.env == Environment.PRODUCTION)

logger = get_logger(__name__)

app = FastAPI(title=settings.app_name)
app.include_router(clients.router)
app.include_router(keys.router)
app.include_router(scopes.router)
app.include_router(demo.router)

register_exception_handlers(app)


@app.get("/")
async def root():
    return {
        "service": "API Key Manager",
        "docs": "https://api-key-manager.piksi.dev/docs",
    }
