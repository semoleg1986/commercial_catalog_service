# Формат Ошибок

## Базовый Формат

HTTP API использует RFC7807 (`application/problem+json`).

Базовые поля:
- `type`
- `title`
- `status`
- `detail`
- `instance`
- `trace_id`

## Доменные Ошибки V1

- `course_not_found`
- `offer_not_found`
- `bundle_offer_not_found`
- `offer_code_conflict`
- `default_offer_conflict`
- `inactive_offer_not_sellable`
- `invalid_price_snapshot`
- `bundle_component_not_found`
- `bundle_components_empty`

## Правила Маппинга

- validation errors -> `422`
- not found -> `404`
- role/access denied -> `403`
- auth missing/invalid -> `401`
- domain conflicts -> `409`
