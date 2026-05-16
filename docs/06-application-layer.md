# Application Слой

## Назначение

Application-слой оркестрирует use cases коммерческого каталога, координирует репозитории через порты и предоставляет единый `ApplicationFacade` для interface-адаптеров.

## Структура Application

```shell
src/application/
|- offers/
|  |- commands/
|  |- queries/
|  `- handlers/
|- bundles/
|  |- commands/
|  |- queries/
|  `- handlers/
|- catalog/
|  `- queries/
|- facade/
|  `- application_facade.py
`- ports/
   |- repositories.py
   |- unit_of_work.py
   |- id_generator.py
   |- clock.py
   `- external_clients.py
```

## Command Side (write)

- offers: `CreateCourseOffer`, `UpdateCourseOffer`, `ActivateCourseOffer`, `DeactivateCourseOffer`, `AssignDefaultCourseOffer`
- bundles: `CreateBundleOffer`, `UpdateBundleOffer`, `ActivateBundleOffer`, `DeactivateBundleOffer`

## Query Side (read)

- `ListPublicCatalogOffers`
- `GetCourseOffers`
- `GetBundleOffers`
- `GetOfferSnapshot`
- `ResolveOfferForCheckout`

## Контракт Фасада

`ApplicationFacade` — единственная точка входа для interface-слоя:
- принимает типизированные command/query DTO
- делегирует в use-case handlers
- возвращает типизированные DTO или доменные ошибки

## Порты И Транзакции

- `UnitOfWork` инкапсулирует транзакцию и репозитории
- `CourseCatalogReader` читает минимальный академический snapshot из `course_service`
- `ClockPort` определяет активность price/label по времени

## Границы Слоя

- без HTTP/ORM типов в application
- без бизнес-инвариантов в interface
- без инфраструктурных реализаций в domain
