# Ubiquitous Language

## Основные Термины

- **Course** — учебная сущность из `course_service`, описывающая содержание и образовательную структуру
- **Course Offer** — коммерческий вариант покупки одного курса
- **Bundle Offer** — коммерческий вариант покупки набора offer
- **Offer Code** — стабильный код коммерческого варианта (`standard`, `homework_review`, `teacher_led`)
- **Offer Price** — витринная цена offer: `list_price`, `sale_price`, `currency`
- **Offer Availability** — признак, доступен ли offer для показа и продажи
- **Promo Label** — короткая маркетинговая метка для витрины (`Хит`, `-20%`, `Семейный пакет`)
- **Offer Component** — элемент состава bundle-offer
- **Default Offer** — offer, показываемый первым для курса в каталоге
- **Catalog Card** — read DTO карточки публичной витрины
- **Offer Details View** — read DTO списка offer для страницы курса

## Термины, Которые Не Смешиваем

- `Course` и `Offer` — не одно и то же
- `Offer` и `OrderLine` — не одно и то же
- `PromoLabel` и pricing rule — не одно и то же
- `BundleOffer` и dynamic mix-and-match rule — не одно и то же
- `Catalog price` и final checkout price — не одно и то же

## Коммерческие Варианты V1

- `standard`
- `homework_review`
- `teacher_led`

## Ограничения Терминологии V1

- `discounted` — это pricing state, а не category
- `popular` — это merchandising collection, а не academic taxonomy
- `teacher_led` — это offer type, а не category курса
