from __future__ import annotations

from dataclasses import dataclass

from src.application.dto import (
    GetCourseOffersQuery,
    GetInternalBundleSnapshotQuery,
    GetInternalOfferSnapshotQuery,
    ListPublicBundlesQuery,
    ListPublicCatalogOffersQuery,
    UpsertInternalCourseOfferCommand,
)
from src.domain import CourseOffer, OfferAvailability, OfferPrice
from src.domain.errors import DefaultOfferConflictError, NotFoundError, ValidationError


@dataclass(slots=True)
class CommercialCatalogFacade:
    uow_factory: callable

    def list_public_catalog_offers(self, _: ListPublicCatalogOffersQuery):
        with self.uow_factory() as uow:
            return uow.course_offer_reads.list_public_catalog_cards()

    def get_course_offers(self, query: GetCourseOffersQuery):
        if not query.course_id.strip():
            raise ValidationError("course_id обязателен.")
        with self.uow_factory() as uow:
            view = uow.course_offer_reads.get_public_course_offers(query.course_id)
        if view is None:
            raise NotFoundError("Course offers не найдены.")
        return view

    def list_public_bundles(self, _: ListPublicBundlesQuery):
        with self.uow_factory() as uow:
            return uow.bundle_offer_reads.list_public_bundles()

    def get_internal_offer_snapshot(self, query: GetInternalOfferSnapshotQuery):
        if not query.offer_id.strip():
            raise ValidationError("offer_id обязателен.")
        with self.uow_factory() as uow:
            offer = uow.course_offer_reads.get_internal_offer_snapshot(query.offer_id)
        if offer is None:
            raise NotFoundError("Offer не найден.")
        return offer

    def get_internal_bundle_snapshot(self, query: GetInternalBundleSnapshotQuery):
        if not query.bundle_offer_id.strip():
            raise ValidationError("bundle_offer_id обязателен.")
        with self.uow_factory() as uow:
            bundle = uow.bundle_offer_reads.get_internal_bundle_snapshot(
                query.bundle_offer_id
            )
        if bundle is None:
            raise NotFoundError("Bundle offer не найден.")
        return bundle

    def upsert_internal_course_offer(self, command: UpsertInternalCourseOfferCommand):
        if not command.offer_id.strip():
            raise ValidationError("offer_id обязателен.")
        if not command.course_id.strip():
            raise ValidationError("course_id обязателен.")
        if not command.offer_code.strip():
            raise ValidationError("offer_code обязателен.")
        if not command.title.strip():
            raise ValidationError("title обязателен.")
        if not command.description_short.strip():
            raise ValidationError("description_short обязателен.")

        offer = CourseOffer(
            offer_id=command.offer_id,
            course_id=command.course_id,
            offer_code=command.offer_code,
            title=command.title,
            description_short=command.description_short,
            sort_order=command.sort_order,
            delivery_mode=command.delivery_mode,
            teacher_included=command.teacher_included,
            homework_review_included=command.homework_review_included,
            availability=OfferAvailability(is_active=command.is_active),
            price=OfferPrice(
                currency=command.currency,
                list_price=command.list_price,
                sale_price=command.sale_price,
            ),
            is_default=command.is_default,
        )

        with self.uow_factory() as uow:
            existing_default = uow.course_offers.get_default_by_course_id(
                command.course_id
            )
            if (
                command.is_default
                and existing_default is not None
                and existing_default.offer_id != command.offer_id
            ):
                raise DefaultOfferConflictError(
                    "course already has a different default offer"
                )

            existing_offer = uow.course_offers.get_by_id(command.offer_id)
            if existing_offer is None:
                uow.course_offers.add(offer)
            else:
                uow.course_offers.save(offer)
            uow.commit()

        return offer
