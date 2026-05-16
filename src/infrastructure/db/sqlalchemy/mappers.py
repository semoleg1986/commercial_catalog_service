from __future__ import annotations

from src.application.ports.external_clients import CourseSnapshot
from src.application.ports.repositories import CatalogCourseCard, CourseOffersView
from src.domain import (
    BundleOffer,
    CourseOffer,
    OfferAvailability,
    OfferComponent,
    OfferPrice,
    PromoLabel,
)
from src.infrastructure.db.sqlalchemy.models import (
    BundleOfferComponentModel,
    BundleOfferModel,
    BundleOfferPromoLabelModel,
    CourseOfferModel,
    CourseOfferPromoLabelModel,
)


def course_offer_to_model(offer: CourseOffer) -> CourseOfferModel:
    model = CourseOfferModel(
        offer_id=offer.offer_id,
        course_id=offer.course_id,
        offer_code=offer.offer_code,
        title=offer.title,
        description_short=offer.description_short,
        sort_order=offer.sort_order,
        delivery_mode=offer.delivery_mode,
        teacher_included=offer.teacher_included,
        homework_review_included=offer.homework_review_included,
        is_active=offer.availability.is_active,
        is_default=offer.is_default,
        sellable_from=offer.availability.sellable_from,
        sellable_to=offer.availability.sellable_to,
        currency=offer.price.currency,
        list_price=offer.price.list_price,
        sale_price=offer.price.sale_price,
        discount_reason=offer.price.discount_reason,
        price_starts_at=offer.price.starts_at,
        price_ends_at=offer.price.ends_at,
        promo_labels=[
            CourseOfferPromoLabelModel(
                label=label.label,
                kind=label.kind,
                position=index,
                starts_at=label.starts_at,
                ends_at=label.ends_at,
            )
            for index, label in enumerate(offer.promo_labels)
        ],
    )
    return model


def model_to_course_offer(model: CourseOfferModel) -> CourseOffer:
    return CourseOffer(
        offer_id=model.offer_id,
        course_id=model.course_id,
        offer_code=model.offer_code,
        title=model.title,
        description_short=model.description_short,
        sort_order=model.sort_order,
        delivery_mode=model.delivery_mode,
        teacher_included=model.teacher_included,
        homework_review_included=model.homework_review_included,
        availability=OfferAvailability(
            is_active=model.is_active,
            sellable_from=model.sellable_from,
            sellable_to=model.sellable_to,
        ),
        price=OfferPrice(
            currency=model.currency,
            list_price=model.list_price,
            sale_price=model.sale_price,
            discount_reason=model.discount_reason,
            starts_at=model.price_starts_at,
            ends_at=model.price_ends_at,
        ),
        promo_labels=tuple(
            PromoLabel(
                label=label.label,
                kind=label.kind,
                starts_at=label.starts_at,
                ends_at=label.ends_at,
            )
            for label in model.promo_labels
        ),
        is_default=model.is_default,
    )


def bundle_offer_to_model(bundle_offer: BundleOffer) -> BundleOfferModel:
    model = BundleOfferModel(
        bundle_offer_id=bundle_offer.bundle_offer_id,
        title=bundle_offer.title,
        description_short=bundle_offer.description_short,
        sort_order=bundle_offer.sort_order,
        is_active=bundle_offer.availability.is_active,
        is_default=bundle_offer.is_default,
        sellable_from=bundle_offer.availability.sellable_from,
        sellable_to=bundle_offer.availability.sellable_to,
        currency=bundle_offer.price.currency,
        list_price=bundle_offer.price.list_price,
        sale_price=bundle_offer.price.sale_price,
        discount_reason=bundle_offer.price.discount_reason,
        price_starts_at=bundle_offer.price.starts_at,
        price_ends_at=bundle_offer.price.ends_at,
        components=[
            BundleOfferComponentModel(
                offer_id=component.offer_id,
                quantity=component.quantity,
                position=component.position,
            )
            for component in bundle_offer.components
        ],
        promo_labels=[
            BundleOfferPromoLabelModel(
                label=label.label,
                kind=label.kind,
                position=index,
                starts_at=label.starts_at,
                ends_at=label.ends_at,
            )
            for index, label in enumerate(bundle_offer.promo_labels)
        ],
    )
    return model


def model_to_bundle_offer(model: BundleOfferModel) -> BundleOffer:
    return BundleOffer(
        bundle_offer_id=model.bundle_offer_id,
        title=model.title,
        description_short=model.description_short,
        sort_order=model.sort_order,
        availability=OfferAvailability(
            is_active=model.is_active,
            sellable_from=model.sellable_from,
            sellable_to=model.sellable_to,
        ),
        price=OfferPrice(
            currency=model.currency,
            list_price=model.list_price,
            sale_price=model.sale_price,
            discount_reason=model.discount_reason,
            starts_at=model.price_starts_at,
            ends_at=model.price_ends_at,
        ),
        components=tuple(
            OfferComponent(
                offer_id=component.offer_id,
                quantity=component.quantity,
                position=component.position,
            )
            for component in model.components
        ),
        promo_labels=tuple(
            PromoLabel(
                label=label.label,
                kind=label.kind,
                starts_at=label.starts_at,
                ends_at=label.ends_at,
            )
            for label in model.promo_labels
        ),
        is_default=model.is_default,
    )


def to_catalog_course_card(
    course_snapshot: CourseSnapshot,
    default_offer: CourseOffer,
    offers_count: int,
) -> CatalogCourseCard:
    return CatalogCourseCard(
        course_id=course_snapshot.course_id,
        title=course_snapshot.title,
        description_short=course_snapshot.description_short,
        level=course_snapshot.level,
        lessons_count=course_snapshot.lessons_count,
        default_offer=default_offer,
        offers_count=offers_count,
    )


def to_course_offers_view(
    course_snapshot: CourseSnapshot,
    offers: tuple[CourseOffer, ...],
) -> CourseOffersView:
    return CourseOffersView(
        course_id=course_snapshot.course_id,
        title=course_snapshot.title,
        description=course_snapshot.description,
        level=course_snapshot.level,
        offers=offers,
    )
