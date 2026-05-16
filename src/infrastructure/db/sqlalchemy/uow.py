from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from src.application.ports.external_clients import CourseCatalogReader
from src.infrastructure.db.sqlalchemy.bundle_offer_repository_sqlalchemy import (
    SqlAlchemyBundleOfferReadRepository,
    SqlAlchemyBundleOfferRepository,
)
from src.infrastructure.db.sqlalchemy.course_offer_repository_sqlalchemy import (
    SqlAlchemyCourseOfferReadRepository,
    SqlAlchemyCourseOfferRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        course_reader: CourseCatalogReader,
    ) -> None:
        self._session_factory = session_factory
        self._course_reader = course_reader
        self._session: Session | None = None
        self.course_offers: SqlAlchemyCourseOfferRepository
        self.bundle_offers: SqlAlchemyBundleOfferRepository
        self.course_offer_reads: SqlAlchemyCourseOfferReadRepository
        self.bundle_offer_reads: SqlAlchemyBundleOfferReadRepository

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        self.course_offers = SqlAlchemyCourseOfferRepository(self._session)
        self.bundle_offers = SqlAlchemyBundleOfferRepository(self._session)
        self.course_offer_reads = SqlAlchemyCourseOfferReadRepository(
            self._session,
            self._course_reader,
        )
        self.bundle_offer_reads = SqlAlchemyBundleOfferReadRepository(self._session)
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        try:
            if self._session is not None and exc is not None:
                self._session.rollback()
        finally:
            if self._session is not None:
                self._session.close()
            self._session = None

    def commit(self) -> None:
        if self._session is not None:
            self._session.commit()

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()
