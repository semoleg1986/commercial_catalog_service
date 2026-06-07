from __future__ import annotations

from fastapi import APIRouter, Depends, status

from src.application.dto import (
    GetInternalBundleSnapshotQuery,
    GetInternalCourseOffersQuery,
    GetInternalDefaultOfferStatusQuery,
    GetInternalOfferSnapshotQuery,
    UpsertInternalCourseOfferCommand,
)
from src.interface.http.common.internal_auth import require_service_token
from src.interface.http.v1.internal.schemas import (
    BundleComponentResponse,
    InternalBundleSnapshotResponse,
    InternalCourseOffersResponse,
    InternalDefaultOfferStatusResponse,
    InternalOfferSnapshotResponse,
    MoneyResponse,
    OfferFeatureFlagsResponse,
    UpsertInternalCourseOfferRequest,
)
from src.interface.http.wiring import get_facade

router = APIRouter(
    prefix="/internal/v1",
    tags=["internal"],
    dependencies=[Depends(require_service_token)],
)


def _to_internal_offer_response(offer) -> InternalOfferSnapshotResponse:
    return InternalOfferSnapshotResponse(
        offer_id=offer.offer_id,
        course_id=offer.course_id,
        offer_code=offer.offer_code,
        title=offer.title,
        description_short=offer.description_short,
        is_default=offer.is_default,
        is_active=offer.availability.is_active,
        price=MoneyResponse(
            currency=offer.price.currency,
            list_price=offer.price.list_price,
            sale_price=offer.price.sale_price,
            discount_reason=offer.price.discount_reason,
        ),
        feature_flags=OfferFeatureFlagsResponse(
            delivery_mode=offer.delivery_mode,
            teacher_included=offer.teacher_included,
            homework_review_included=offer.homework_review_included,
        ),
    )


@router.get("/offers/{offer_id}", response_model=InternalOfferSnapshotResponse)
def get_offer_snapshot(
    offer_id: str,
    facade=Depends(get_facade),
) -> InternalOfferSnapshotResponse:
    offer = facade.get_internal_offer_snapshot(
        GetInternalOfferSnapshotQuery(offer_id=offer_id)
    )
    return _to_internal_offer_response(offer)


@router.get(
    "/courses/{course_id}/offers",
    response_model=InternalCourseOffersResponse,
)
def list_course_offers(
    course_id: str,
    facade=Depends(get_facade),
) -> InternalCourseOffersResponse:
    offers = facade.list_internal_course_offers(
        GetInternalCourseOffersQuery(course_id=course_id)
    )
    return InternalCourseOffersResponse(
        course_id=course_id,
        offers=[_to_internal_offer_response(offer) for offer in offers],
    )


@router.get(
    "/courses/{course_id}/default-offer-status",
    response_model=InternalDefaultOfferStatusResponse,
)
def get_default_offer_status(
    course_id: str,
    facade=Depends(get_facade),
) -> InternalDefaultOfferStatusResponse:
    has_offer = facade.get_internal_default_offer_status(
        GetInternalDefaultOfferStatusQuery(course_id=course_id)
    )
    return InternalDefaultOfferStatusResponse(
        course_id=course_id,
        has_active_default_offer=has_offer,
    )


@router.get(
    "/bundles/{bundle_offer_id}",
    response_model=InternalBundleSnapshotResponse,
)
def get_bundle_snapshot(
    bundle_offer_id: str,
    facade=Depends(get_facade),
) -> InternalBundleSnapshotResponse:
    bundle = facade.get_internal_bundle_snapshot(
        GetInternalBundleSnapshotQuery(bundle_offer_id=bundle_offer_id)
    )
    return InternalBundleSnapshotResponse(
        bundle_offer_id=bundle.bundle_offer_id,
        title=bundle.title,
        is_active=bundle.availability.is_active,
        price=MoneyResponse(
            currency=bundle.price.currency,
            list_price=bundle.price.list_price,
            sale_price=bundle.price.sale_price,
            discount_reason=bundle.price.discount_reason,
        ),
        components=[
            BundleComponentResponse(
                offer_id=component.offer_id,
                quantity=component.quantity,
                position=component.position,
            )
            for component in bundle.components
        ],
    )


@router.post(
    "/course-offers",
    response_model=InternalOfferSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
)
def upsert_course_offer(
    request: UpsertInternalCourseOfferRequest,
    facade=Depends(get_facade),
) -> InternalOfferSnapshotResponse:
    offer = facade.upsert_internal_course_offer(
        UpsertInternalCourseOfferCommand(
            offer_id=request.offer_id,
            course_id=request.course_id,
            offer_code=request.offer_code,
            title=request.title,
            description_short=request.description_short,
            currency=request.currency,
            list_price=request.list_price,
            sale_price=request.sale_price,
            sort_order=request.sort_order,
            delivery_mode=request.delivery_mode,
            teacher_included=request.teacher_included,
            homework_review_included=request.homework_review_included,
            is_active=request.is_active,
            is_default=request.is_default,
        )
    )
    return _to_internal_offer_response(offer)
