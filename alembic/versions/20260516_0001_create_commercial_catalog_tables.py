"""create commercial catalog tables

Revision ID: 20260516_0001
Revises:
Create Date: 2026-05-16
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260516_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "course_offers",
        sa.Column("offer_id", sa.String(length=64), primary_key=True),
        sa.Column("course_id", sa.String(length=64), nullable=False),
        sa.Column("offer_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description_short", sa.Text(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("delivery_mode", sa.String(length=32), nullable=False),
        sa.Column("teacher_included", sa.Boolean(), nullable=False),
        sa.Column("homework_review_included", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("sellable_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sellable_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("list_price", sa.Float(), nullable=False),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("discount_reason", sa.String(length=128), nullable=True),
        sa.Column("price_starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("price_ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "course_id",
            "offer_code",
            name="uq_course_offers_course_offer_code",
        ),
    )
    op.create_index("ix_course_offers_course_id", "course_offers", ["course_id"])
    op.create_index("ix_course_offers_is_active", "course_offers", ["is_active"])

    op.create_table(
        "course_offer_promo_labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("offer_id", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["course_offers.offer_id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        "ix_course_offer_promo_labels_offer_id",
        "course_offer_promo_labels",
        ["offer_id"],
    )

    op.create_table(
        "bundle_offers",
        sa.Column("bundle_offer_id", sa.String(length=64), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description_short", sa.Text(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("sellable_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sellable_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("list_price", sa.Float(), nullable=False),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("discount_reason", sa.String(length=128), nullable=True),
        sa.Column("price_starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("price_ends_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_bundle_offers_is_active", "bundle_offers", ["is_active"])

    op.create_table(
        "bundle_offer_components",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("bundle_offer_id", sa.String(length=64), nullable=False),
        sa.Column("offer_id", sa.String(length=64), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(
            ["bundle_offer_id"],
            ["bundle_offers.bundle_offer_id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        "ix_bundle_offer_components_bundle_offer_id",
        "bundle_offer_components",
        ["bundle_offer_id"],
    )
    op.create_index(
        "ix_bundle_offer_components_offer_id",
        "bundle_offer_components",
        ["offer_id"],
    )

    op.create_table(
        "bundle_offer_promo_labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("bundle_offer_id", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["bundle_offer_id"],
            ["bundle_offers.bundle_offer_id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        "ix_bundle_offer_promo_labels_bundle_offer_id",
        "bundle_offer_promo_labels",
        ["bundle_offer_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_bundle_offer_promo_labels_bundle_offer_id",
        table_name="bundle_offer_promo_labels",
    )
    op.drop_table("bundle_offer_promo_labels")
    op.drop_index(
        "ix_bundle_offer_components_offer_id",
        table_name="bundle_offer_components",
    )
    op.drop_index(
        "ix_bundle_offer_components_bundle_offer_id",
        table_name="bundle_offer_components",
    )
    op.drop_table("bundle_offer_components")
    op.drop_index("ix_bundle_offers_is_active", table_name="bundle_offers")
    op.drop_table("bundle_offers")
    op.drop_index(
        "ix_course_offer_promo_labels_offer_id",
        table_name="course_offer_promo_labels",
    )
    op.drop_table("course_offer_promo_labels")
    op.drop_index("ix_course_offers_is_active", table_name="course_offers")
    op.drop_index("ix_course_offers_course_id", table_name="course_offers")
    op.drop_table("course_offers")
