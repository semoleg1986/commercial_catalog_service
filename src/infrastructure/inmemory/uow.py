from __future__ import annotations

from src.application.ports.external_clients import CourseCatalogReader
from src.domain import BundleOffer, CourseOffer
from src.infrastructure.inmemory.repositories import (
    InMemoryBundleOfferReadRepository,
    InMemoryBundleOfferRepository,
    InMemoryCourseOfferReadRepository,
    InMemoryCourseOfferRepository,
)


class InMemoryUnitOfWork:
    def __init__(
        self,
        *,
        offers: dict[str, CourseOffer],
        bundle_offers: dict[str, BundleOffer],
        course_reader: CourseCatalogReader,
    ) -> None:
        self._offers = offers
        self._bundle_offers = bundle_offers
        self._course_reader = course_reader

    def __enter__(self) -> "InMemoryUnitOfWork":
        self.course_offers = InMemoryCourseOfferRepository(self._offers)
        self.bundle_offers = InMemoryBundleOfferRepository(self._bundle_offers)
        self.course_offer_reads = InMemoryCourseOfferReadRepository(
            self._offers,
            self._course_reader,
        )
        self.bundle_offer_reads = InMemoryBundleOfferReadRepository(self._bundle_offers)
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None
