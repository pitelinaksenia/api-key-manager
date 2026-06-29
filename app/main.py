from fastapi import FastAPI

from app.api.routes import clients, keys, scopes
from app.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(clients.router)
app.include_router(keys.router)
app.include_router(scopes.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
