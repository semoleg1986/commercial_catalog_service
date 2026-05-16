from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.sqlalchemy.base import Base


class CourseOfferModel(Base):
    __tablename__ = "course_offers"

    offer_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    course_id: Mapped[str] = mapped_column(String(64), index=True)
    offer_code: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    description_short: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    delivery_mode: Mapped[str] = mapped_column(String(32), default="online")
    teacher_included: Mapped[bool] = mapped_column(Boolean, default=False)
    homework_review_included: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    sellable_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sellable_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    currency: Mapped[str] = mapped_column(String(3))
    list_price: Mapped[float] = mapped_column(Float)
    sale_price: Mapped[float] = mapped_column(Float)
    discount_reason: Mapped[str | None] = mapped_column(String(128))
    price_starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    price_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    promo_labels: Mapped[list[CourseOfferPromoLabelModel]] = relationship(
        back_populates="offer",
        cascade="all, delete-orphan",
        order_by="CourseOfferPromoLabelModel.position",
    )


class CourseOfferPromoLabelModel(Base):
    __tablename__ = "course_offer_promo_labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    offer_id: Mapped[str] = mapped_column(
        ForeignKey("course_offers.offer_id", ondelete="CASCADE"),
        index=True,
    )
    label: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(64))
    position: Mapped[int] = mapped_column(Integer, default=0)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    offer: Mapped[CourseOfferModel] = relationship(back_populates="promo_labels")


class BundleOfferModel(Base):
    __tablename__ = "bundle_offers"

    bundle_offer_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description_short: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    sellable_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sellable_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    currency: Mapped[str] = mapped_column(String(3))
    list_price: Mapped[float] = mapped_column(Float)
    sale_price: Mapped[float] = mapped_column(Float)
    discount_reason: Mapped[str | None] = mapped_column(String(128))
    price_starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    price_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    components: Mapped[list[BundleOfferComponentModel]] = relationship(
        back_populates="bundle_offer",
        cascade="all, delete-orphan",
        order_by="BundleOfferComponentModel.position",
    )
    promo_labels: Mapped[list[BundleOfferPromoLabelModel]] = relationship(
        back_populates="bundle_offer",
        cascade="all, delete-orphan",
        order_by="BundleOfferPromoLabelModel.position",
    )


class BundleOfferComponentModel(Base):
    __tablename__ = "bundle_offer_components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bundle_offer_id: Mapped[str] = mapped_column(
        ForeignKey("bundle_offers.bundle_offer_id", ondelete="CASCADE"),
        index=True,
    )
    offer_id: Mapped[str] = mapped_column(String(64), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    position: Mapped[int] = mapped_column(Integer, default=0)

    bundle_offer: Mapped[BundleOfferModel] = relationship(back_populates="components")


class BundleOfferPromoLabelModel(Base):
    __tablename__ = "bundle_offer_promo_labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bundle_offer_id: Mapped[str] = mapped_column(
        ForeignKey("bundle_offers.bundle_offer_id", ondelete="CASCADE"),
        index=True,
    )
    label: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(64))
    position: Mapped[int] = mapped_column(Integer, default=0)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    bundle_offer: Mapped[BundleOfferModel] = relationship(back_populates="promo_labels")
