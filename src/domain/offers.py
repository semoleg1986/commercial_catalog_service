from __future__ import annotations

from dataclasses import dataclass

from src.domain.errors import (
    DefaultOfferConflictError,
    EmptyBundleError,
    InactiveDefaultOfferError,
    InvalidBundleComponentError,
)
from src.domain.value_objects import OfferAvailability, OfferPrice, PromoLabel


@dataclass(frozen=True, slots=True)
class CourseOffer:
    offer_id: str
    course_id: str
    offer_code: str
    title: str
    description_short: str
    sort_order: int
    delivery_mode: str
    teacher_included: bool
    homework_review_included: bool
    availability: OfferAvailability
    price: OfferPrice
    promo_labels: tuple[PromoLabel, ...] = ()
    is_default: bool = False

    def __post_init__(self) -> None:
        if not self.offer_id.strip():
            raise DefaultOfferConflictError("offer_id cannot be empty")
        if not self.course_id.strip():
            raise DefaultOfferConflictError("course_id cannot be empty")
        if not self.offer_code.strip():
            raise DefaultOfferConflictError("offer_code cannot be empty")
        if not self.title.strip():
            raise DefaultOfferConflictError("title cannot be empty")
        if self.sort_order < 0:
            raise DefaultOfferConflictError("sort_order cannot be negative")
        if self.is_default and not self.availability.is_active:
            raise InactiveDefaultOfferError(
                "inactive offer cannot be marked as default"
            )


@dataclass(frozen=True, slots=True)
class OfferComponent:
    offer_id: str
    quantity: int
    position: int

    def __post_init__(self) -> None:
        if not self.offer_id.strip():
            raise InvalidBundleComponentError("component offer_id cannot be empty")
        if self.quantity <= 0:
            raise InvalidBundleComponentError("component quantity must be positive")
        if self.position < 0:
            raise InvalidBundleComponentError("component position cannot be negative")


@dataclass(frozen=True, slots=True)
class BundleOffer:
    bundle_offer_id: str
    title: str
    description_short: str
    sort_order: int
    availability: OfferAvailability
    price: OfferPrice
    components: tuple[OfferComponent, ...]
    promo_labels: tuple[PromoLabel, ...] = ()
    is_default: bool = False

    def __post_init__(self) -> None:
        if not self.bundle_offer_id.strip():
            raise EmptyBundleError("bundle_offer_id cannot be empty")
        if not self.title.strip():
            raise EmptyBundleError("bundle title cannot be empty")
        if self.sort_order < 0:
            raise EmptyBundleError("sort_order cannot be negative")
        if not self.components:
            raise EmptyBundleError("bundle must contain at least one component")
        if self.is_default and not self.availability.is_active:
            raise InactiveDefaultOfferError(
                "inactive bundle cannot be marked as default"
            )


def ensure_single_default_course_offer(offers: tuple[CourseOffer, ...]) -> None:
    default_count = sum(1 for offer in offers if offer.is_default)
    if default_count > 1:
        raise DefaultOfferConflictError(
            "course cannot have more than one default offer"
        )
