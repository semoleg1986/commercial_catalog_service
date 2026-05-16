from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListPublicCatalogOffersQuery:
    pass


@dataclass(frozen=True, slots=True)
class GetCourseOffersQuery:
    course_id: str


@dataclass(frozen=True, slots=True)
class ListPublicBundlesQuery:
    pass


@dataclass(frozen=True, slots=True)
class GetInternalOfferSnapshotQuery:
    offer_id: str


@dataclass(frozen=True, slots=True)
class GetInternalBundleSnapshotQuery:
    bundle_offer_id: str
