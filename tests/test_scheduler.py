import pytest
from src.python.scheduler.course import Course
from src.python.scheduler.scheduler import DegreeScheduler


def test_scheduler_generates_valid_schedule():
    """Test that scheduler generates a valid schedule."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("CS201", "Data Structures", 4, {"CS101"}, 2.0),
        Course("CS301", "Algorithms", 4, {"CS201"}, 3.0),
        Course("MATH101", "Calculus I", 4, set(), 2.0),
        Course("MATH201", "Linear Algebra", 4, {"MATH101"}, 2.0),
    ]

    scheduler = DegreeScheduler(courses)
    schedule = scheduler.schedule(target_credits_per_semester=12.0, num_semesters=8)

    # Check that schedule has correct number of semesters
    assert len(schedule) == 8

    # Check that all courses are scheduled
    scheduled_courses = set()
    for semester in schedule:
        for course in semester:
            scheduled_courses.add(course.code)

    assert scheduled_courses == {"CS101", "CS201", "CS301", "MATH101", "MATH201"}


def test_scheduler_respects_prerequisites():
    """Test that scheduler respects course prerequisites."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("CS201", "Data Structures", 4, {"CS101"}, 2.0),
    ]

    scheduler = DegreeScheduler(courses)
    schedule = scheduler.schedule()

    # Find positions of courses
    cs101_semester = None
    cs201_semester = None

    for sem_idx, semester in enumerate(schedule):
        for course in semester:
            if course.code == "CS101":
                cs101_semester = sem_idx
            elif course.code == "CS201":
                cs201_semester = sem_idx

    assert cs101_semester is not None
    assert cs201_semester is not None
    assert cs101_semester < cs201_semester


def test_scheduler_credit_balance():
    """Test that scheduler balances credits per semester."""
    courses = [
        Course(f"C{i}", f"Course {i}", (i % 3) + 2, set(), float((i % 3) + 1))
        for i in range(1, 6)
    ]

    scheduler = DegreeScheduler(courses)
    schedule = scheduler.schedule(target_credits_per_semester=8.0)

    # Check credit distribution
    for semester in schedule:
        credits = sum(c.credits for c in semester)
        if credits > 0:
            assert credits <= 8.0


def test_schedule_summary():
    """Test that schedule summary is generated correctly."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("MATH101", "Calculus", 4, set(), 2.0),
    ]

    scheduler = DegreeScheduler(courses)
    schedule = scheduler.schedule()
    summary = scheduler.get_schedule_summary(schedule)

    assert "PERSONALIZED 4-YEAR DEGREE PLAN" in summary
    assert "CS101" in summary
    assert "MATH101" in summary
    assert "TOTAL CREDITS" in summary
