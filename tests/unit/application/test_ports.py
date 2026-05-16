from src.application import ClockPort, CourseCatalogReader, UnitOfWork
from src.application.ports.external_clients import CourseSnapshot
from src.application.ports.repositories import CatalogCourseCard, CourseOffersView


def test_course_snapshot_shape():
    snapshot = CourseSnapshot(
        course_id="course-1",
        title="Math",
        description="Math course",
        description_short="Short",
        level="beginner",
        lessons_count=12,
        is_published=True,
    )

    assert snapshot.course_id == "course-1"
    assert snapshot.lessons_count == 12


def test_ports_are_importable():
    assert ClockPort is not None
    assert CourseCatalogReader is not None
    assert UnitOfWork is not None
    assert CatalogCourseCard is not None
    assert CourseOffersView is not None
