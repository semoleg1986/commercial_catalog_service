# commercial_catalog_service

Commercial catalog service for public offers.

## Responsibility

`commercial_catalog_service` owns:
- public offer cards
- course offers and bundle offers
- promo labels and offer composition
- public catalog read model consumed by `web_app`

It does not own the course content itself; it integrates with `course_service` for course snapshots.

## Local run

### Install
```bash
make install
```

### Run
```bash
make run
```

### Health
```bash
curl -fsS http://127.0.0.1:8007/healthz
```

## Environment

Primary settings are defined in:
- [settings.py](/Users/olegsemenov/Programming/curs/commercial_catalog_service/src/infrastructure/config/settings.py)

Key variables:
- `COMMERCIAL_CATALOG_APP_PORT`
- `COMMERCIAL_CATALOG_DATABASE_URL`
- `COMMERCIAL_CATALOG_USE_INMEMORY`
- `COMMERCIAL_CATALOG_SERVICE_TOKEN`
- `COMMERCIAL_CATALOG_COURSE_SERVICE_BASE_URL`
- `COMMERCIAL_CATALOG_COURSE_SERVICE_TOKEN`

## Tests and quality

```bash
make test
make lint
make format
```

## Migrations

```bash
make migrate
```

## Documentation

- [00-vision.md](/Users/olegsemenov/Programming/curs/commercial_catalog_service/docs/00-vision.md)
- [08-interface-layer.md](/Users/olegsemenov/Programming/curs/commercial_catalog_service/docs/08-interface-layer.md)
- [09-infrastructure-layer.md](/Users/olegsemenov/Programming/curs/commercial_catalog_service/docs/09-infrastructure-layer.md)
