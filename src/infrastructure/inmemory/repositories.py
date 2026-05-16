from __future__ import annotations

from collections import defaultdict

from src.application.ports.external_clients import CourseCatalogReader, CourseSnapshot
from src.application.ports.repositories import (
    BundleOfferReadRepository,
    BundleOfferRepository,
    CatalogCourseCard,
    CourseOfferReadRepository,
    CourseOfferRepository,
    CourseOffersView,
)
from src.domain import BundleOffer, CourseOffer
from src.infrastructure.db.sqlalchemy.mappers import (
    to_catalog_course_card,
    to_course_offers_view,
)


class InMemoryCourseOfferRepository(CourseOfferRepository):
    def __init__(self, offers: dict[str, CourseOffer]) -> None:
        self._offers = offers

    def add(self, offer: CourseOffer) -> None:
        self._offers[offer.offer_id] = offer

    def save(self, offer: CourseOffer) -> None:
        self._offers[offer.offer_id] = offer

    def get_by_id(self, offer_id: str) -> CourseOffer | None:
        return self._offers.get(offer_id)

    def list_by_course_id(self, course_id: str) -> tuple[CourseOffer, ...]:
        items = [
            offer for offer in self._offers.values() if offer.course_id == course_id
        ]
        return tuple(
            sorted(items, key=lambda offer: (offer.sort_order, offer.offer_code))
        )

    def exists_offer_code(self, course_id: str, offer_code: str) -> bool:
        return any(
            offer.course_id == course_id and offer.offer_code == offer_code
            for offer in self._offers.values()
        )

    def get_default_by_course_id(self, course_id: str) -> CourseOffer | None:
        for offer in self.list_by_course_id(course_id):
            if offer.is_default:
                return offer
        return None


class InMemoryBundleOfferRepository(BundleOfferRepository):
    def __init__(self, bundle_offers: dict[str, BundleOffer]) -> None:
        self._bundle_offers = bundle_offers

    def add(self, bundle_offer: BundleOffer) -> None:
        self._bundle_offers[bundle_offer.bundle_offer_id] = bundle_offer

    def save(self, bundle_offer: BundleOffer) -> None:
        self._bundle_offers[bundle_offer.bundle_offer_id] = bundle_offer

    def get_by_id(self, bundle_offer_id: str) -> BundleOffer | None:
        return self._bundle_offers.get(bundle_offer_id)

    def list_active(self) -> tuple[BundleOffer, ...]:
        items = [
            bundle
            for bundle in self._bundle_offers.values()
            if bundle.availability.is_active
        ]
        return tuple(
            sorted(items, key=lambda bundle: (bundle.sort_order, bundle.title))
        )


class InMemoryCourseOfferReadRepository(CourseOfferReadRepository):
    def __init__(
        self,
        offers: dict[str, CourseOffer],
        course_reader: CourseCatalogReader,
    ) -> None:
        self._offers = offers
        self._course_reader = course_reader

    def list_public_catalog_cards(self) -> tuple[CatalogCourseCard, ...]:
        grouped: dict[str, list[CourseOffer]] = defaultdict(list)
        for offer in self._offers.values():
            if offer.availability.is_active:
                grouped[offer.course_id].append(offer)

        cards: list[CatalogCourseCard] = []
        for course_id, offers in grouped.items():
            snapshot = self._course_reader.get_course_snapshot(course_id)
            if snapshot is None or not snapshot.is_published:
                continue
            ordered = sorted(
                offers, key=lambda item: (item.sort_order, item.offer_code)
            )
            default_offer = next((item for item in ordered if item.is_default), None)
            if default_offer is None:
                continue
            cards.append(
                to_catalog_course_card(
                    course_snapshot=snapshot,
                    default_offer=default_offer,
                    offers_count=len(ordered),
                )
            )
        return tuple(
            sorted(cards, key=lambda card: (card.default_offer.sort_order, card.title))
        )

    def get_public_course_offers(self, course_id: str) -> CourseOffersView | None:
        snapshot = self._course_reader.get_course_snapshot(course_id)
        if snapshot is None or not snapshot.is_published:
            return None
        offers = tuple(
            sorted(
                [
                    offer
                    for offer in self._offers.values()
                    if offer.course_id == course_id and offer.availability.is_active
                ],
                key=lambda item: (item.sort_order, item.offer_code),
            )
        )
        return to_course_offers_view(snapshot, offers)

    def get_internal_offer_snapshot(self, offer_id: str) -> CourseOffer | None:
        return self._offers.get(offer_id)


class InMemoryBundleOfferReadRepository(BundleOfferReadRepository):
    def __init__(self, bundle_offers: dict[str, BundleOffer]) -> None:
        self._bundle_offers = bundle_offers

    def list_public_bundles(self) -> tuple[BundleOffer, ...]:
        items = [
            bundle
            for bundle in self._bundle_offers.values()
            if bundle.availability.is_active
        ]
        return tuple(
            sorted(items, key=lambda bundle: (bundle.sort_order, bundle.title))
        )

    def get_internal_bundle_snapshot(self, bundle_offer_id: str) -> BundleOffer | None:
        return self._bundle_offers.get(bundle_offer_id)


class InMemoryCourseCatalogReader(CourseCatalogReader):
    def __init__(self, snapshots: dict[str, CourseSnapshot]) -> None:
        self._snapshots = snapshots

    def get_course_snapshot(self, course_id: str) -> CourseSnapshot | None:
        return self._snapshots.get(course_id)

    def list_published_course_snapshots(self) -> tuple[CourseSnapshot, ...]:
        return tuple(
            snapshot for snapshot in self._snapshots.values() if snapshot.is_published
        )
