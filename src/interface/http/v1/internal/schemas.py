from __future__ import annotations

from pydantic import BaseModel


class MoneyResponse(BaseModel):
    currency: str
    list_price: float
    sale_price: float
    discount_reason: str | None = None


class OfferFeatureFlagsResponse(BaseModel):
    delivery_mode: str
    teacher_included: bool
    homework_review_included: bool


class BundleComponentResponse(BaseModel):
    offer_id: str
    quantity: int
    position: int


class InternalOfferSnapshotResponse(BaseModel):
    offer_id: str
    course_id: str
    offer_code: str
    title: str
    is_active: bool
    price: MoneyResponse
    feature_flags: OfferFeatureFlagsResponse


class InternalBundleSnapshotResponse(BaseModel):
    bundle_offer_id: str
    title: str
    is_active: bool
    price: MoneyResponse
    components: list[BundleComponentResponse]


class UpsertInternalCourseOfferRequest(BaseModel):
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
