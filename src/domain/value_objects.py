from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.errors import InvalidMoneyAmountError


@dataclass(frozen=True, slots=True)
class OfferPrice:
    currency: str
    list_price: float
    sale_price: float
    discount_reason: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    def __post_init__(self) -> None:
        currency = self.currency.strip().upper()
        object.__setattr__(self, "currency", currency)
        if len(currency) != 3:
            raise InvalidMoneyAmountError("currency must be a 3-letter code")
        if self.list_price < 0 or self.sale_price < 0:
            raise InvalidMoneyAmountError("price amounts must be non-negative")
        if self.sale_price > self.list_price:
            raise InvalidMoneyAmountError("sale_price cannot exceed list_price")
        if self.starts_at and self.ends_at and self.starts_at > self.ends_at:
            raise InvalidMoneyAmountError("starts_at cannot be later than ends_at")


@dataclass(frozen=True, slots=True)
class OfferAvailability:
    is_active: bool
    sellable_from: datetime | None = None
    sellable_to: datetime | None = None

    def __post_init__(self) -> None:
        if (
            self.sellable_from
            and self.sellable_to
            and self.sellable_from > self.sellable_to
        ):
            raise InvalidMoneyAmountError(
                "sellable_from cannot be later than sellable_to"
            )


@dataclass(frozen=True, slots=True)
class PromoLabel:
    label: str
    kind: str
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    def __post_init__(self) -> None:
        label = self.label.strip()
        kind = self.kind.strip()
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "kind", kind)
        if not label:
            raise InvalidMoneyAmountError("promo label cannot be empty")
        if not kind:
            raise InvalidMoneyAmountError("promo label kind cannot be empty")
        if self.starts_at and self.ends_at and self.starts_at > self.ends_at:
            raise InvalidMoneyAmountError(
                "promo label starts_at cannot be later than ends_at"
            )


def normalize_labels(labels: tuple[PromoLabel, ...]) -> tuple[PromoLabel, ...]:
    return tuple(labels)
