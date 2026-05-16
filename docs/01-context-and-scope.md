# Bounded Context И Границы

## Название Контекста

**Контекст Коммерческого Каталога**

## Назначение Контекста

Контекст управляет коммерческой проекцией учебных продуктов.
Он определяет, какие offer доступны к продаже, какие bundle существуют, какую цену и промо-метки видит пользователь и какой offer lookup использует checkout.

## Ответственность

Контекст обязан:
1. управлять жизненным циклом `CourseOffer`
2. управлять жизненным циклом `BundleOffer`
3. хранить текущую публичную цену (`list_price`, `sale_price`, `currency`)
4. предоставлять публичный catalog/details read API
5. предоставлять internal offer lookup для downstream checkout
6. публиковать стабильную модель коммерческой витрины для UI

## Структура Агрегатов

```shell
CourseOffer (Aggregate Root)
|- OfferPrice (Value Object)
|- OfferAvailability (Value Object)
`- PromoLabel (Value Object)

BundleOffer (Aggregate Root)
|- OfferPrice (Value Object)
|- OfferAvailability (Value Object)
|- PromoLabel (Value Object)
`- OfferComponent (Entity)
```

## Внешние Зависимости

Зависит от:
- `course_service` для проверки существования `Course` и получения академических snapshot-полей
- persistence адаптеров через порты

Не зависит от:
- деталей HTTP-фреймворка в domain/application
- прямого доступа к checkout/order данным
- бонусного кошелька и payment orchestration

## Границы С Соседними Сервисами

### `course_service`

`course_service` владеет:
- `Course`
- структурой модулей и уроков
- publish-state учебного контента
- progress/completion

`commercial_catalog_service` владеет:
- коммерческими вариантами продажи курса
- bundle-предложениями
- витринной ценой и promo label

Правило:
- `commercial_catalog_service` ссылается на `course_id`
- `course_service` не владеет `Offer` и не считает price/promotion

### `payments_service`

`payments_service` владеет:
- `Cart`
- `Quote`
- `Order`
- `PaymentIntent`
- final pricing snapshot checkout

`commercial_catalog_service` владеет:
- базовым catalog price и availability
- составом bundle
- offer metadata для выбора на витрине

Правило:
- `payments_service` не становится source of truth для catalog offer
- `payments_service` читает `offer_id` и snapshot-поля из `commercial_catalog_service`

## Точки Интеграции

Входящие:
- admin-операции по заведению/обновлению offer
- public read-запросы витрины
- internal lookup от checkout

Исходящие:
- downstream уведомление о смене offer-модели позже через outbox/events
- сейчас baseline допускает только synchronous read-contract
