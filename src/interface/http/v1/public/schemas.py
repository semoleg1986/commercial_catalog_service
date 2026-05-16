from __future__ import annotations

from pydantic import BaseModel


class MoneyResponse(BaseModel):
    currency: str
    list_price: float
    sale_price: float
    discount_reason: str | None = None


class PromoLabelResponse(BaseModel):
    label: str
    kind: str


class OfferFeatureFlagsResponse(BaseModel):
    delivery_mode: str
    teacher_included: bool
    homework_review_included: bool


class OfferResponse(BaseModel):
    offer_id: str
    offer_code: str
    title: str
    description_short: str
    price: MoneyResponse
    promo_labels: list[PromoLabelResponse]
    feature_flags: OfferFeatureFlagsResponse


class CatalogCourseCardResponse(BaseModel):
    course_id: str
    title: str
    description_short: str
    level: str
    lessons_count: int
    default_offer: OfferResponse
    offers_count: int


class PublicCatalogResponse(BaseModel):
    items: list[CatalogCourseCardResponse]


class CourseSummaryResponse(BaseModel):
    course_id: str
    title: str
    description: str
    level: str


class CourseOffersResponse(BaseModel):
    course: CourseSummaryResponse
    offers: list[OfferResponse]


class BundleComponentResponse(BaseModel):
    offer_id: str
    quantity: int
    position: int


class BundleOfferResponse(BaseModel):
    bundle_offer_id: str
    title: str
    description_short: str
    price: MoneyResponse
    promo_labels: list[PromoLabelResponse]
    components: list[BundleComponentResponse]


class PublicBundleListResponse(BaseModel):
    items: list[BundleOfferResponse]
