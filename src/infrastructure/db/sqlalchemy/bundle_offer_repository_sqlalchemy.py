from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.application.ports.repositories import (
    BundleOfferReadRepository,
    BundleOfferRepository,
)
from src.domain import BundleOffer
from src.infrastructure.db.sqlalchemy.mappers import (
    bundle_offer_to_model,
    model_to_bundle_offer,
)
from src.infrastructure.db.sqlalchemy.models import (
    BundleOfferComponentModel,
    BundleOfferModel,
    BundleOfferPromoLabelModel,
)


class SqlAlchemyBundleOfferRepository(BundleOfferRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, bundle_offer: BundleOffer) -> None:
        self._session.add(bundle_offer_to_model(bundle_offer))

    def save(self, bundle_offer: BundleOffer) -> None:
        stmt = (
            select(BundleOfferModel)
            .where(BundleOfferModel.bundle_offer_id == bundle_offer.bundle_offer_id)
            .options(
                selectinload(BundleOfferModel.components),
                selectinload(BundleOfferModel.promo_labels),
            )
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        if model is None:
            self.add(bundle_offer)
            return

        model.title = bundle_offer.title
        model.description_short = bundle_offer.description_short
        model.sort_order = bundle_offer.sort_order
        model.is_active = bundle_offer.availability.is_active
        model.is_default = bundle_offer.is_default
        model.sellable_from = bundle_offer.availability.sellable_from
        model.sellable_to = bundle_offer.availability.sellable_to
        model.currency = bundle_offer.price.currency
        model.list_price = bundle_offer.price.list_price
        model.sale_price = bundle_offer.price.sale_price
        model.discount_reason = bundle_offer.price.discount_reason
        model.price_starts_at = bundle_offer.price.starts_at
        model.price_ends_at = bundle_offer.price.ends_at
        model.components[:] = [
            BundleOfferComponentModel(
                offer_id=component.offer_id,
                quantity=component.quantity,
                position=component.position,
            )
            for component in bundle_offer.components
        ]
        model.promo_labels[:] = [
            BundleOfferPromoLabelModel(
                label=label.label,
                kind=label.kind,
                position=index,
                starts_at=label.starts_at,
                ends_at=label.ends_at,
            )
            for index, label in enumerate(bundle_offer.promo_labels)
        ]

    def get_by_id(self, bundle_offer_id: str) -> BundleOffer | None:
        stmt = (
            select(BundleOfferModel)
            .where(BundleOfferModel.bundle_offer_id == bundle_offer_id)
            .options(
                selectinload(BundleOfferModel.components),
                selectinload(BundleOfferModel.promo_labels),
            )
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else model_to_bundle_offer(model)

    def list_active(self) -> tuple[BundleOffer, ...]:
        stmt = (
            select(BundleOfferModel)
            .where(BundleOfferModel.is_active.is_(True))
            .order_by(BundleOfferModel.sort_order, BundleOfferModel.title)
            .options(
                selectinload(BundleOfferModel.components),
                selectinload(BundleOfferModel.promo_labels),
            )
        )
        return tuple(
            model_to_bundle_offer(model)
            for model in self._session.execute(stmt).scalars()
        )


class SqlAlchemyBundleOfferReadRepository(BundleOfferReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_public_bundles(self) -> tuple[BundleOffer, ...]:
        return self._list_active_bundles_only()

    def get_internal_bundle_snapshot(self, bundle_offer_id: str) -> BundleOffer | None:
        stmt = (
            select(BundleOfferModel)
            .where(BundleOfferModel.bundle_offer_id == bundle_offer_id)
            .options(
                selectinload(BundleOfferModel.components),
                selectinload(BundleOfferModel.promo_labels),
            )
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else model_to_bundle_offer(model)

    def _list_active_bundles_only(self) -> tuple[BundleOffer, ...]:
        stmt = (
            select(BundleOfferModel)
            .where(BundleOfferModel.is_active.is_(True))
            .order_by(BundleOfferModel.sort_order, BundleOfferModel.title)
            .options(
                selectinload(BundleOfferModel.components),
                selectinload(BundleOfferModel.promo_labels),
            )
        )
        return tuple(
            model_to_bundle_offer(model)
            for model in self._session.execute(stmt).scalars()
        )
