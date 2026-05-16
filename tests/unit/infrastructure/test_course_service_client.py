from src.infrastructure.clients.course_service_client import (
    _course_snapshot_from_catalog_item,
    _course_snapshot_from_payload,
)


def test_course_snapshot_from_payload_uses_description_fallbacks():
    snapshot = _course_snapshot_from_payload(
        {
            "course_id": "course-1",
            "title": "Math",
            "description": "Long description",
            "level": "beginner",
            "lessons_count": 7,
            "is_published": True,
        }
    )

    assert snapshot.course_id == "course-1"
    assert snapshot.description_short == "Long description"
    assert snapshot.lessons_count == 7
    assert snapshot.is_published is True


def test_course_snapshot_from_catalog_item_marks_snapshot_published():
    snapshot = _course_snapshot_from_catalog_item(
        {
            "course_id": "course-2",
            "title": "Science",
            "description_short": "Short",
            "level": "intermediate",
            "lessons_count": 12,
        }
    )

    assert snapshot.course_id == "course-2"
    assert snapshot.description_short == "Short"
    assert snapshot.is_published is True
