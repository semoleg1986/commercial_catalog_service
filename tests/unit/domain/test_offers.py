import pytest

from src.domain import (
    BundleOffer,
    CourseOffer,
    DefaultOfferConflictError,
    EmptyBundleError,
    InactiveDefaultOfferError,
    InvalidBundleComponentError,
    InvalidMoneyAmountError,
    OfferAvailability,
    OfferComponent,
    OfferPrice,
    PromoLabel,
    ensure_single_default_course_offer,
)


def test_offer_price_rejects_sale_price_above_list_price():
    with pytest.raises(InvalidMoneyAmountError):
        OfferPrice(currency="usd", list_price=100, sale_price=120)


def test_course_offer_rejects_inactive_default_offer():
    with pytest.raises(InactiveDefaultOfferError):
        CourseOffer(
            offer_id="offer-1",
            course_id="course-1",
            offer_code="standard",
            title="Standard",
            description_short="Basic offer",
            sort_order=0,
            delivery_mode="online",
            teacher_included=False,
            homework_review_included=False,
            availability=OfferAvailability(is_active=False),
            price=OfferPrice(currency="usd", list_price=100, sale_price=80),
            is_default=True,
        )


def test_bundle_offer_requires_components():
    with pytest.raises(EmptyBundleError):
        BundleOffer(
            bundle_offer_id="bundle-1",
            title="Family bundle",
            description_short="Two courses",
            sort_order=0,
            availability=OfferAvailability(is_active=True),
            price=OfferPrice(currency="usd", list_price=200, sale_price=150),
            components=(),
        )


def test_offer_component_requires_positive_quantity():
    with pytest.raises(InvalidBundleComponentError):
        OfferComponent(offer_id="offer-1", quantity=0, position=0)


def test_single_default_offer_policy_rejects_duplicates():
    availability = OfferAvailability(is_active=True)
    price = OfferPrice(currency="usd", list_price=100, sale_price=90)
    labels = (PromoLabel(label="-10%", kind="discount"),)
    first = CourseOffer(
        offer_id="offer-1",
        course_id="course-1",
        offer_code="standard",
        title="Standard",
        description_short="Basic",
        sort_order=0,
        delivery_mode="online",
        teacher_included=False,
        homework_review_included=False,
        availability=availability,
        price=price,
        promo_labels=labels,
        is_default=True,
    )
    second = CourseOffer(
        offer_id="offer-2",
        course_id="course-1",
        offer_code="teacher_led",
        title="Teacher-led",
        description_short="Premium",
        sort_order=1,
        delivery_mode="online",
        teacher_included=True,
        homework_review_included=True,
        availability=availability,
        price=price,
        is_default=True,
    )

    with pytest.raises(DefaultOfferConflictError):
        ensure_single_default_course_offer((first, second))
