# Инварианты И Политики

## Инварианты Offer

1. `CourseOffer` всегда привязан к существующему `course_id`
2. в рамках одного курса `offer_code` уникален
3. только один `CourseOffer` на курс может быть `is_default = true`
4. inactive offer не участвует в public catalog
5. `sale_price` не может быть больше `list_price`

## Инварианты Bundle

1. bundle должен содержать минимум один компонент
2. bundle не может ссылаться на несуществующий `offer_id`
3. inactive component-offer не делает bundle автоматически валидным для продажи без явной policy
4. bundle-price не должен вычисляться в UI; сервис отдает готовый snapshot

## Политики Публикации Витрины

1. public catalog показывает только active offer
2. если у курса нет active default offer, курс не попадает в public catalog baseline
3. old/new price показываются только как snapshot-поля read model
4. promo label не является источником истины о скидке; это display metadata

## Политики Границ

1. `course_service` не пишет в БД `commercial_catalog_service`
2. `payments_service` не хранит catalog source-of-truth у себя
3. интерфейсные адаптеры не считают цену самостоятельно
4. final checkout price может отличаться от catalog price после бонусов, referral, bundle logic и future promotions
