# Infrastructure Слой

## Назначение

Infrastructure-слой реализует выходные адаптеры для application-портов.
Слой заменяем без изменений в domain/application.

## Структура

```shell
src/infrastructure/
|- db/
|  |- session.py
|  |- models.py
|  |- mappers.py
|  |- repositories/
|  |  |- course_offer_repository_sqlalchemy.py
|  |  `- bundle_offer_repository_sqlalchemy.py
|  `- uow/sqlalchemy_uow.py
|- clients/
|  `- course_service_client.py
|- messaging/
|  `- outbox_publisher.py
`- di/
   `- providers.py
```

## Ответственность

- реализовать репозитории и `UnitOfWork`
- реализовать клиент чтения course snapshot из `course_service`
- реализовать outbox/event publishing позже
- собрать DI composition root для runtime

## Правила Границ

- без HTTP-контрактов в infrastructure
- без use-case orchestration в infrastructure
- без доменных policy-решений в infrastructure
