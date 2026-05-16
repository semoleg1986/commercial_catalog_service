from __future__ import annotations

from typing import Protocol

from src.application.ports.repositories import (
    BundleOfferReadRepository,
    BundleOfferRepository,
    CourseOfferReadRepository,
    CourseOfferRepository,
)


class UnitOfWork(Protocol):
    course_offers: CourseOfferRepository
    bundle_offers: BundleOfferRepository
    course_offer_reads: CourseOfferReadRepository
    bundle_offer_reads: BundleOfferReadRepository

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(self, exc_type, exc, tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
