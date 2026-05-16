# Interface Слой

## Назначение

Interface-слой описывает transport contracts, валидацию запросов и маппинг ошибок для API-клиентов.
Слой зависит только от application facade и DTO-контрактов.

## Структура

```shell
src/interface/http/
|- app.py
|- main.py
|- health.py
|- errors.py
|- problem_types.py
|- wiring.py
`- v1/
   |- public/router.py
   |- admin/router.py
   |- internal/router.py
   `- schemas/
      |- offers.py
      |- bundles.py
      `- catalog.py
```

## Ответственность

- строить transport adapters (HTTP сейчас, gRPC/CLI позже)
- валидировать request DTO
- маппить application-ошибки в RFC7807
- извлекать actor context и вызывать `ApplicationFacade`
- предоставлять public-endpoints витрины
- предоставлять internal-endpoints для `payments_service`
- предоставлять admin-endpoints управления offer позже

## Public API Baseline

- `GET /v1/public/catalog/offers`
- `GET /v1/public/courses/{course_id}/offers`
- `GET /v1/public/bundles`

## Internal API Baseline

- `GET /internal/v1/offers/{offer_id}`
- `GET /internal/v1/bundles/{bundle_offer_id}`

## Правила Границ

- без SQLAlchemy/session usage
- без доменной логики инвариантов
- без прямого доступа к репозиториям
