# Архитектурное Видение Commercial Catalog Service

## Назначение

`commercial_catalog_service` — bounded context для коммерческого описания продаваемых учебных продуктов.
Сервис владеет offer-моделью, bundle-моделью, прайсинговыми snapshot-полями витрины и метаданными промо-показа.

Ключевые цели:
- отделить учебную сущность `Course` от коммерческой сущности `Offer`
- держать коммерческие варианты курса в одном месте
- предоставлять стабильный read-контракт для `web_app`, `admin_app` и `payments_service`
- сохранить независимость `course_service` от pricing/promotions/bundles

## Бизнес-ценность

Сервис обеспечивает:
- единый источник истины по продаваемым вариантам курса
- поддержку old/new price presentation
- поддержку статических bundle-offer
- базу для временных акций и promo label
- предсказуемый контракт для будущего `cart/order` в `payments_service`

## Границы

### Входит в контекст
- `CourseOffer`
- `BundleOffer`
- `OfferComponent`
- `OfferPrice`
- `OfferAvailability`
- `PromoLabel`
- read-модель catalog/details для публичной витрины

### Не входит в контекст
- учебный контент и структура курса (`course_service`)
- корзина, checkout, quote, order, payment intent (`payments_service`)
- бонусный кошелек и списание бонусов (`bonus_wallet_service`)
- referral attribution и conversion analytics (`attribution-service`)
- аутентификация и lifecycle access token (`auth_service`)

## Принципы

- Commercial model first: `Offer` не смешивается с `Course`
- Явные границы: без cross-service доступа в БД
- Clean Architecture: domain/application не зависят от HTTP/ORM
- Read contracts first: публичная витрина и internal-lookup контракты стабилизируются до cart/order
- Эволюция без слома: новые pricing rules не должны ломать базовый `Offer` read contract
