from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from src.application.ports.external_clients import CourseCatalogReader, CourseSnapshot


@dataclass(frozen=True, slots=True)
class CourseServiceClientConfig:
    base_url: str
    service_token: str | None = None
    timeout_seconds: float = 2.0


class CourseServiceHttpClient(CourseCatalogReader):
    def __init__(self, config: CourseServiceClientConfig) -> None:
        self._config = config

    def get_course_snapshot(self, course_id: str) -> CourseSnapshot | None:
        payload = self._get_json(f"/v1/public/courses/{quote(course_id)}")
        if payload is None:
            return None
        return _course_snapshot_from_payload(payload)

    def list_published_course_snapshots(self) -> tuple[CourseSnapshot, ...]:
        payload = self._get_json("/v1/public/catalog")
        if payload is None:
            return ()
        items = payload.get("items", [])
        return tuple(
            _course_snapshot_from_catalog_item(item)
            for item in items
            if isinstance(item, dict)
        )

    def _get_json(self, path: str) -> dict[str, Any] | None:
        url = f"{self._config.base_url.rstrip('/')}{path}"
        headers: dict[str, str] = {"Accept": "application/json"}
        if self._config.service_token:
            headers["Authorization"] = f"Bearer {self._config.service_token}"
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=self._config.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                return None
            raise
        except URLError:
            return None


def _course_snapshot_from_payload(payload: dict[str, Any]) -> CourseSnapshot:
    return CourseSnapshot(
        course_id=str(payload.get("course_id", "")),
        title=str(payload.get("title", "")),
        description=str(payload.get("description", "")),
        description_short=str(
            payload.get("description_short") or payload.get("description", "")
        ),
        level=str(payload.get("level", "")),
        lessons_count=int(payload.get("lessons_count", 0) or 0),
        is_published=bool(payload.get("is_published", True)),
    )


def _course_snapshot_from_catalog_item(item: dict[str, Any]) -> CourseSnapshot:
    return CourseSnapshot(
        course_id=str(item.get("course_id", "")),
        title=str(item.get("title", "")),
        description=str(item.get("description", "")),
        description_short=str(
            item.get("description_short") or item.get("description", "")
        ),
        level=str(item.get("level", "")),
        lessons_count=int(item.get("lessons_count", 0) or 0),
        is_published=True,
    )
