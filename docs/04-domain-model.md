# Domain Model

## Aggregate: CourseOffer

`CourseOffer` — корневая сущность коммерческого варианта одного курса.

### Поля V1

- `offer_id`
- `course_id`
- `offer_code`
- `title`
- `description_short`
- `is_active`
- `is_default`
- `sort_order`
- `delivery_mode`
- `teacher_included`
- `homework_review_included`
- `price`
- `promo_labels`

### Инварианты

- `course_id` обязателен
- `offer_code` уникален в рамках курса
- default offer у курса не может быть больше одного
- inactive offer не может быть выбран как default
- `sale_price <= list_price`

## Aggregate: BundleOffer

`BundleOffer` — корневая сущность коммерческого набора из одного или нескольких offer.

### Поля V1

- `bundle_offer_id`
- `title`
- `description_short`
- `is_active`
- `is_default`
- `sort_order`
- `price`
- `promo_labels`
- `components`

### Component

`OfferComponent` содержит:
- `offer_id`
- `quantity`
- `position`

### Инварианты

- bundle должен содержать хотя бы один компонент
- компонент должен ссылаться на существующий offer
- `sale_price <= list_price`

## Value Objects

### OfferPrice

- `currency`
- `list_price`
- `sale_price`
- `discount_reason`
- `starts_at`
- `ends_at`

### OfferAvailability

- `is_active`
- `sellable_from`
- `sellable_to`

### PromoLabel

- `label`
- `kind`
- `starts_at`
- `ends_at`

## Read Model

Публичная витрина не читает доменные агрегаты напрямую.
Она использует стабильные read DTO:
- `CatalogCourseCard`
- `CourseOffersView`
- `BundleOfferView`
