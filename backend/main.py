"""
Application factory. Trimmed: see backend/README.md.

The point of interest is that `DEPLOYMENT_MODE` decides which routers are
mounted at all. Unlinking a route from the UI leaves it reachable, so a public
deployment must not mount it — absence is the control, not authorization.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create any missing tables, warm the caches, then hand over.
    ...
    yield
    # Dispose of engines and clients.
    ...


def create_app() -> FastAPI:
    app = FastAPI(title="Financial Intelligence Pipeline", lifespan=lifespan)

    # Mounted in every mode: the query route and health.
    app.include_router(financial_router)
    app.include_router(health_router)

    if settings.DEPLOYMENT_MODE == "full":
        # Nine further routers, each behind a role check: admin, SQL, vector,
        # ingestion, evaluation, escalation, claims, security, auth.
        ...

    return app


app = create_app()
