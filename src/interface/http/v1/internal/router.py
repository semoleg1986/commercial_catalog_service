from __future__ import annotations

from fastapi import APIRouter, Depends

from src.application.dto import (
    GetInternalBundleSnapshotQuery,
    GetInternalOfferSnapshotQuery,
)
from src.interface.http.common.internal_auth import require_service_token
from src.interface.http.v1.internal.schemas import (
    BundleComponentResponse,
    InternalBundleSnapshotResponse,
    InternalOfferSnapshotResponse,
    MoneyResponse,
    OfferFeatureFlagsResponse,
)
from src.interface.http.wiring import get_facade

router = APIRouter(
    prefix="/internal/v1",
    tags=["internal"],
    dependencies=[Depends(require_service_token)],
)


@router.get("/offers/{offer_id}", response_model=InternalOfferSnapshotResponse)
def get_offer_snapshot(
    offer_id: str,
    facade=Depends(get_facade),
) -> InternalOfferSnapshotResponse:
    offer = facade.get_internal_offer_snapshot(
        GetInternalOfferSnapshotQuery(offer_id=offer_id)
    )
    return InternalOfferSnapshotResponse(
        offer_id=offer.offer_id,
        course_id=offer.course_id,
        offer_code=offer.offer_code,
        title=offer.title,
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
