from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.domain import BundleOffer, CourseOffer


@dataclass(frozen=True, slots=True)
class CatalogCourseCard:
    course_id: str
    title: str
    description_short: str
    level: str
    lessons_count: int
    default_offer: CourseOffer
    offers_count: int


@dataclass(frozen=True, slots=True)
class CourseOffersView:
    course_id: str
    title: str
    description: str
    level: str
    offers: tuple[CourseOffer, ...]


class CourseOfferRepository(Protocol):
    def add(self, offer: CourseOffer) -> None:
        ...

    def save(self, offer: CourseOffer) -> None:
        ...

    def get_by_id(self, offer_id: str) -> CourseOffer | None:
        ...

    def list_by_course_id(self, course_id: str) -> tuple[CourseOffer, ...]:
        ...

    def exists_offer_code(self, course_id: str, offer_code: str) -> bool:
        ...

    def get_default_by_course_id(self, course_id: str) -> CourseOffer | None:
        ...


class BundleOfferRepository(Protocol):
    def add(self, bundle_offer: BundleOffer) -> None:
        ...

    def save(self, bundle_offer: BundleOffer) -> None:
        ...

    def get_by_id(self, bundle_offer_id: str) -> BundleOffer | None:
        ...

    def list_active(self) -> tuple[BundleOffer, ...]:
        ...


class CourseOfferReadRepository(Protocol):
    def list_public_catalog_cards(self) -> tuple[CatalogCourseCard, ...]:
        ...

    def get_public_course_offers(self, course_id: str) -> CourseOffersView | None:
        ...

    def get_internal_offer_snapshot(self, offer_id: str) -> CourseOffer | None:
        ...


class BundleOfferReadRepository(Protocol):
    def list_public_bundles(self) -> tuple[BundleOffer, ...]:
        ...

    def get_internal_bundle_snapshot(self, bundle_offer_id: str) -> BundleOffer | None:
        ...
