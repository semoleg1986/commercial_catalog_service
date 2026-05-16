from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.application.ports.external_clients import CourseCatalogReader
from src.application.ports.repositories import (
    CatalogCourseCard,
    CourseOfferReadRepository,
    CourseOfferRepository,
    CourseOffersView,
)
from src.domain import CourseOffer
from src.infrastructure.db.sqlalchemy.mappers import (
    course_offer_to_model,
    model_to_course_offer,
    to_catalog_course_card,
    to_course_offers_view,
)
from src.infrastructure.db.sqlalchemy.models import CourseOfferModel


class SqlAlchemyCourseOfferRepository(CourseOfferRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, offer: CourseOffer) -> None:
        self._session.add(course_offer_to_model(offer))

    def save(self, offer: CourseOffer) -> None:
        model = self._session.execute(
            select(CourseOfferModel)
            .where(CourseOfferModel.offer_id == offer.offer_id)
            .options(selectinload(CourseOfferModel.promo_labels))
        ).scalar_one_or_none()
        if model is None:
            self.add(offer)
            return

        model.course_id = offer.course_id
        model.offer_code = offer.offer_code
        model.title = offer.title
        model.description_short = offer.description_short
        model.sort_order = offer.sort_order
        model.delivery_mode = offer.delivery_mode
        model.teacher_included = offer.teacher_included
        model.homework_review_included = offer.homework_review_included
        model.is_active = offer.availability.is_active
        model.is_default = offer.is_default
        model.sellable_from = offer.availability.sellable_from
        model.sellable_to = offer.availability.sellable_to
        model.currency = offer.price.currency
        model.list_price = offer.price.list_price
        model.sale_price = offer.price.sale_price
        model.discount_reason = offer.price.discount_reason
        model.price_starts_at = offer.price.starts_at
        model.price_ends_at = offer.price.ends_at
        model.promo_labels[:] = []
        for mapper in course_offer_to_model(offer).promo_labels:
            model.promo_labels.append(mapper)

    def get_by_id(self, offer_id: str) -> CourseOffer | None:
        stmt = (
            select(CourseOfferModel)
            .where(CourseOfferModel.offer_id == offer_id)
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else model_to_course_offer(model)

    def list_by_course_id(self, course_id: str) -> tuple[CourseOffer, ...]:
        stmt = (
            select(CourseOfferModel)
            .where(CourseOfferModel.course_id == course_id)
            .order_by(CourseOfferModel.sort_order, CourseOfferModel.offer_code)
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        return tuple(
            model_to_course_offer(model)
            for model in self._session.execute(stmt).scalars()
        )

    def exists_offer_code(self, course_id: str, offer_code: str) -> bool:
        stmt = select(CourseOfferModel.offer_id).where(
            CourseOfferModel.course_id == course_id,
            CourseOfferModel.offer_code == offer_code,
        )
        return self._session.execute(stmt).first() is not None

    def get_default_by_course_id(self, course_id: str) -> CourseOffer | None:
        stmt = (
            select(CourseOfferModel)
            .where(
                CourseOfferModel.course_id == course_id,
                CourseOfferModel.is_default.is_(True),
            )
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else model_to_course_offer(model)


class SqlAlchemyCourseOfferReadRepository(CourseOfferReadRepository):
    def __init__(self, session: Session, course_reader: CourseCatalogReader) -> None:
        self._session = session
        self._course_reader = course_reader

    def list_public_catalog_cards(self) -> tuple[CatalogCourseCard, ...]:
        stmt = (
            select(CourseOfferModel)
            .where(
                CourseOfferModel.is_active.is_(True),
                CourseOfferModel.is_default.is_(True),
            )
            .order_by(CourseOfferModel.sort_order, CourseOfferModel.title)
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        cards: list[CatalogCourseCard] = []
        for model in self._session.execute(stmt).scalars():
            snapshot = self._course_reader.get_course_snapshot(model.course_id)
            if snapshot is None or not snapshot.is_published:
                continue
            offers_count = len(self._load_course_offers(model.course_id))
            cards.append(
                to_catalog_course_card(
                    course_snapshot=snapshot,
                    default_offer=model_to_course_offer(model),
                    offers_count=offers_count,
                )
            )
        return tuple(cards)

    def get_public_course_offers(self, course_id: str) -> CourseOffersView | None:
        snapshot = self._course_reader.get_course_snapshot(course_id)
        if snapshot is None or not snapshot.is_published:
            return None
        offers = tuple(
            offer
            for offer in self._load_course_offers(course_id)
            if offer.availability.is_active
        )
        return to_course_offers_view(snapshot, offers)

    def get_internal_offer_snapshot(self, offer_id: str) -> CourseOffer | None:
        stmt = (
            select(CourseOfferModel)
            .where(CourseOfferModel.offer_id == offer_id)
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else model_to_course_offer(model)

    def _load_course_offers(self, course_id: str) -> tuple[CourseOffer, ...]:
        stmt = (
            select(CourseOfferModel)
            .where(CourseOfferModel.course_id == course_id)
            .order_by(CourseOfferModel.sort_order, CourseOfferModel.offer_code)
            .options(selectinload(CourseOfferModel.promo_labels))
        )
        return tuple(
            model_to_course_offer(model)
            for model in self._session.execute(stmt).scalars()
        )
