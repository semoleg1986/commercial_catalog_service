from fastapi import FastAPI

from src.domain.errors import DomainError
from src.interface.http.errors import domain_error_handler, register_exception_handlers
from src.interface.http.health import router as health_router
from src.interface.http.v1.internal.router import router as internal_router
from src.interface.http.v1.public.router import router as public_router


def create_app() -> FastAPI:
    app = FastAPI(title="commercial_catalog_service")
    app.include_router(health_router)
    app.include_router(public_router)
    app.include_router(internal_router)
    app.add_exception_handler(DomainError, domain_error_handler)
    register_exception_handlers(app)
    return app
