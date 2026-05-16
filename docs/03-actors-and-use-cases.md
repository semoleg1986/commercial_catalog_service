# Actors И Use Cases

## Акторы

- `Admin` — управляет коммерческим каталогом
- `Parent / Public Visitor` — читает витрину и выбирает offer
- `payments_service` — внутренний потребитель offer lookup
- `web_app` / `admin_app` — интерфейсные адаптеры поверх публичных и admin-контрактов

## Primary Use Cases

### Admin

1. создать `CourseOffer` для существующего `Course`
2. обновить цену, availability и promo label offer
3. назначить default offer для курса
4. создать `BundleOffer` и состав bundle
5. деактивировать offer без удаления исторической ссылки

### Public / Parent

1. просмотреть catalog card курса с default offer
2. открыть страницу курса и увидеть список доступных offer
3. понять old/new price и базовые коммерческие отличия offer

### `payments_service`

1. разрешить `offer_id` в коммерческий snapshot
2. получить состав `BundleOffer`
3. проверить, доступен ли offer для checkout

## Secondary Use Cases

1. экспорт/синхронизация catalog read model позже
2. публикация offer-changed событий позже
3. future support для временных кампаний и auto-discount rules
