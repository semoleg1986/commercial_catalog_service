# ADR-0001: Bounded Context Для Commercial Catalog Service

## Статус
Принято

## Дата
2026-05-16

## Контекст
Платформа выделяет учебный контент, checkout и loyalty в отдельные сервисы.
Появились требования, которые нельзя аккуратно держать внутри `course_service`:
- несколько коммерческих вариантов одного курса
- old/new price
- promo label
- bundle offer
- future promotions и auto-discount rules

Одновременно cart/order lifecycle слишком близок к checkout и payment orchestration, чтобы выносить его в отдельный сервис заранее.

## Решение
Создается отдельный bounded context `commercial_catalog_service`.

`commercial_catalog_service` владеет:
- `CourseOffer`
- `BundleOffer`
- offer price snapshot (`list_price`, `sale_price`, `currency`)
- offer availability
- promo labels
- составом bundle
- публичной витринной read model

`commercial_catalog_service` не владеет:
- учебной сущностью `Course`
- корзиной, quote, order, payment intent
- бонусным кошельком
- referral attribution analytics

Правила интеграции:
- `course_service` остается source of truth для учебной сущности `Course`
- `payments_service` остается source of truth для `Cart`, `Quote`, `Order`, `PaymentIntent`
- `payments_service` использует `offer_id` и offer snapshot из `commercial_catalog_service`
- прямой доступ к БД со стороны соседних сервисов запрещен

## Последствия
- учебная и коммерческая модели разделены до выхода в production
- будущий cart/order может строиться поверх стабильного `Offer`
- `course_service` не обрастает pricing/promotions логикой
- `payments_service` не становится владельцем catalog source-of-truth
