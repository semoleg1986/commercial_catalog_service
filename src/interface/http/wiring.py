from __future__ import annotations

from functools import lru_cache

from src.application import CommercialCatalogFacade
from src.application.ports.external_clients import CourseSnapshot
from src.infrastructure.clients.course_service_client import (
    CourseServiceClientConfig,
    CourseServiceHttpClient,
)
from src.infrastructure.config.settings import Settings
from src.infrastructure.db.sqlalchemy.base import Base
from src.infrastructure.db.sqlalchemy.session import build_session_factory
from src.infrastructure.db.sqlalchemy.uow import SqlAlchemyUnitOfWork
from src.infrastructure.inmemory.repositories import InMemoryCourseCatalogReader
from src.infrastructure.inmemory.uow import InMemoryUnitOfWork

_OFFERS = {}
_BUNDLE_OFFERS = {}
_COURSE_SNAPSHOTS = {
    "course-smoke-1": CourseSnapshot(
        course_id="course-smoke-1",
        title="Smoke Course",
        description="Seed snapshot for local development.",
        description_short="Seed snapshot",
        level="beginner",
        lessons_count=2,
        is_published=True,
    )
}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()


@lru_cache(maxsize=1)
def get_session_factory():
    settings = get_settings()
    session_factory = build_session_factory(settings.database_url)
    if settings.auto_create_schema:
        engine = session_factory.kw["bind"]
        if engine is not None:
            Base.metadata.create_all(engine)
    return session_factory


@lru_cache(maxsize=1)
def get_course_catalog_reader():
    settings = get_settings()
    if settings.use_inmemory:
        return InMemoryCourseCatalogReader(_COURSE_SNAPSHOTS)
    return CourseServiceHttpClient(
        CourseServiceClientConfig(
            base_url=settings.course_service_base_url,
            service_token=settings.course_service_token,
            timeout_seconds=settings.course_service_timeout_seconds,
        )
    )


def get_facade() -> CommercialCatalogFacade:
    settings = get_settings()
    if settings.use_inmemory:
        return CommercialCatalogFacade(
            uow_factory=lambda: InMemoryUnitOfWork(
                offers=_OFFERS,
                bundle_offers=_BUNDLE_OFFERS,
                course_reader=get_course_catalog_reader(),
            )
        )
    return CommercialCatalogFacade(
        uow_factory=lambda: SqlAlchemyUnitOfWork(
            get_session_factory(),
            get_course_catalog_reader(),
        )
    )


def reset_runtime_state() -> None:
    _OFFERS.clear()
    _BUNDLE_OFFERS.clear()
    _COURSE_SNAPSHOTS.clear()
    get_settings.cache_clear()
    get_session_factory.cache_clear()
    get_course_catalog_reader.cache_clear()
