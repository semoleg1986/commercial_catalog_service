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


@dataclass(frozen=True, slots=True)
class UpsertInternalCourseOfferCommand:
    offer_id: str
    course_id: str
    offer_code: str
    title: str
    description_short: str
    currency: str
    list_price: float
    sale_price: float
    sort_order: int = 0
    delivery_mode: str = "online"
    teacher_included: bool = False
    homework_review_included: bool = False
    is_active: bool = True
    is_default: bool = False
