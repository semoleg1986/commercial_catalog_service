from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class CourseSnapshot:
    course_id: str
    title: str
    description: str
    description_short: str
    level: str
    lessons_count: int
    is_published: bool


class CourseCatalogReader(Protocol):
    def get_course_snapshot(self, course_id: str) -> CourseSnapshot | None:
        """Return minimal academic snapshot from course_service."""

    def list_published_course_snapshots(self) -> tuple[CourseSnapshot, ...]:
        """Return published academic courses eligible for catalog projection."""
