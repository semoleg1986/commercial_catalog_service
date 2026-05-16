from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_host: str
    app_port: int
    database_url: str
    use_inmemory: bool
    auto_create_schema: bool
    service_token: str
    course_service_base_url: str
    course_service_token: str
    course_service_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv(
                "COMMERCIAL_CATALOG_APP_NAME", "commercial_catalog_service"
            ),
            app_host=os.getenv("COMMERCIAL_CATALOG_APP_HOST", "0.0.0.0"),
            app_port=int(os.getenv("COMMERCIAL_CATALOG_APP_PORT", "8007")),
            database_url=os.getenv(
                "COMMERCIAL_CATALOG_DATABASE_URL",
                "sqlite:///./commercial_catalog_service.db",
            ),
            use_inmemory=os.getenv("COMMERCIAL_CATALOG_USE_INMEMORY", "1") == "1",
            auto_create_schema=os.getenv("COMMERCIAL_CATALOG_AUTO_CREATE_SCHEMA", "0")
            == "1",
            service_token=os.getenv(
                "COMMERCIAL_CATALOG_SERVICE_TOKEN",
                "dev-service-token",
            ),
            course_service_base_url=os.getenv(
                "COMMERCIAL_CATALOG_COURSE_SERVICE_BASE_URL",
                "http://localhost:8001",
            ),
            course_service_token=os.getenv(
                "COMMERCIAL_CATALOG_COURSE_SERVICE_TOKEN",
                "dev-service-token",
            ),
            course_service_timeout_seconds=float(
                os.getenv("COMMERCIAL_CATALOG_COURSE_SERVICE_TIMEOUT_SECONDS", "2")
            ),
        )
