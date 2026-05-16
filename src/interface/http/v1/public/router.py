from __future__ import annotations

from fastapi import APIRouter, Depends

from src.application.dto import (
    GetCourseOffersQuery,
    ListPublicBundlesQuery,
    ListPublicCatalogOffersQuery,
)
from src.interface.http.v1.public.schemas import (
    BundleComponentResponse,
    BundleOfferResponse,
    CatalogCourseCardResponse,
    CourseOffersResponse,
    CourseSummaryResponse,
    MoneyResponse,
    OfferFeatureFlagsResponse,
    OfferResponse,
    PromoLabelResponse,
    PublicBundleListResponse,
    PublicCatalogResponse,
)
from src.interface.http.wiring import get_facade

router = APIRouter(prefix="/v1/public", tags=["public"])


@router.get("/catalog/offers", response_model=PublicCatalogResponse)
def list_catalog_offers(facade=Depends(get_facade)) -> PublicCatalogResponse:
    items = facade.list_public_catalog_offers(ListPublicCatalogOffersQuery())
    return PublicCatalogResponse(items=[_to_catalog_card(item) for item in items])


@router.get("/courses/{course_id}/offers", response_model=CourseOffersResponse)
def get_course_offers(
    course_id: str, facade=Depends(get_facade)
) -> CourseOffersResponse:
    view = facade.get_course_offers(GetCourseOffersQuery(course_id=course_id))
    return CourseOffersResponse(
        course=CourseSummaryResponse(
            course_id=view.course_id,
            title=view.title,
            description=view.description,
            level=view.level,
        ),
        offers=[_to_offer_response(item) for item in view.offers],
    )


@router.get("/bundles", response_model=PublicBundleListResponse)
def list_public_bundles(facade=Depends(get_facade)) -> PublicBundleListResponse:
    items = facade.list_public_bundles(ListPublicBundlesQuery())
    return PublicBundleListResponse(
        items=[
            BundleOfferResponse(
                bundle_offer_id=item.bundle_offer_id,
                title=item.title,
                description_short=item.description_short,
                price=_to_money(item),
                promo_labels=_to_labels(item),
                components=[
                    BundleComponentResponse(
                        offer_id=component.offer_id,
                        quantity=component.quantity,
                        position=component.position,
                    )
                    for component in item.components
                ],
            )
            for item in items
        ]
    )


def _to_catalog_card(item) -> CatalogCourseCardResponse:
    return CatalogCourseCardResponse(
        course_id=item.course_id,
        title=item.title,
        description_short=item.description_short,
        level=item.level,
        lessons_count=item.lessons_count,
        default_offer=_to_offer_response(item.default_offer),
        offers_count=item.offers_count,
    )


def _to_offer_response(offer) -> OfferResponse:
    return OfferResponse(
        offer_id=offer.offer_id,
        offer_code=offer.offer_code,
        title=offer.title,
        description_short=offer.description_short,
        price=_to_money(offer),
        promo_labels=_to_labels(offer),
        feature_flags=OfferFeatureFlagsResponse(
            delivery_mode=offer.delivery_mode,
            teacher_included=offer.teacher_included,
            homework_review_included=offer.homework_review_included,
        ),
    )


def _to_money(offer) -> MoneyResponse:
    return MoneyResponse(
        currency=offer.price.currency,
        list_price=offer.price.list_price,
        sale_price=offer.price.sale_price,
        discount_reason=offer.price.discount_reason,
    )


def _to_labels(offer) -> list[PromoLabelResponse]:
    return [
        PromoLabelResponse(label=label.label, kind=label.kind)
        for label in offer.promo_labels
    ]
