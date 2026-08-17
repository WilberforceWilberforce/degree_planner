import pytest
from src.python.scheduler.course import Course
from src.python.scheduler.dag import DAG


def test_dag_topological_sort():
    """Test topological sorting of courses."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("CS201", "Data Structures", 4, {"CS101"}, 2.0),
        Course("CS301", "Algorithms", 4, {"CS201"}, 3.0),
    ]

    dag = DAG(courses)
    topo_order = dag.topological_sort()

    assert topo_order[0] == "CS101"
    assert topo_order.index("CS101") < topo_order.index("CS201")
    assert topo_order.index("CS201") < topo_order.index("CS301")


def test_dag_cycle_detection():
    """Test cycle detection in prerequisites."""
    courses = [
        Course("A", "Course A", 3, {"B"}, 1.0),
        Course("B", "Course B", 3, {"A"}, 1.0),
    ]

    with pytest.raises(ValueError):
        DAG(courses)


def test_can_take_course():
    """Test checking if a course can be taken."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("CS201", "Data Structures", 4, {"CS101"}, 2.0),
    ]

    dag = DAG(courses)

    assert dag.can_take_course("CS101", set())
    assert not dag.can_take_course("CS201", set())
    assert dag.can_take_course("CS201", {"CS101"})


def test_get_available_courses():
    """Test getting available courses."""
    courses = [
        Course("CS101", "Intro to CS", 3, set(), 1.0),
        Course("CS201", "Data Structures", 4, {"CS101"}, 2.0),
        Course("MATH101", "Calculus", 4, set(), 2.0),
    ]

    dag = DAG(courses)

    available = dag.get_available_courses(set())
    assert "CS101" in available
    assert "MATH101" in available
    assert "CS201" not in available

    available = dag.get_available_courses({"CS101"})
    assert "CS201" in available
