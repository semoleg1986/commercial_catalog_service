from __future__ import annotations

from dataclasses import dataclass

from src.application.dto import (
    GetCourseOffersQuery,
    GetInternalBundleSnapshotQuery,
    GetInternalOfferSnapshotQuery,
    ListPublicBundlesQuery,
    ListPublicCatalogOffersQuery,
)
from src.domain.errors import NotFoundError, ValidationError


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
