from typing import Dict, Set, List
from collections import deque
from .course import Course


class DAG:
    """Directed Acyclic Graph for course prerequisites."""

    def __init__(self, courses: List[Course]):
        """Initialize DAG with courses."""
        self.courses = {course.code: course for course in courses}
        self.graph = self._build_graph()
        self._detect_cycle()

    def _build_graph(self) -> Dict[str, Set[str]]:
        """Build adjacency list for the DAG."""
        graph = {course.code: course.prerequisites for course in self.courses.values()}
        return graph

    def _detect_cycle(self) -> None:
        """Detect cycles in the DAG using DFS."""
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for course in self.courses:
            if course not in visited:
                if has_cycle(course):
                    raise ValueError("Cycle detected in course prerequisites")

    def topological_sort(self) -> List[str]:
        """Generate topological ordering of courses using Kahn's algorithm."""
        in_degree = {course: len(self.graph[course]) for course in self.courses}
        queue = deque([course for course in self.courses if in_degree[course] == 0])
        topo_order = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            # Find all courses that depend on this one
            for course in self.courses:
                if node in self.graph[course]:
                    in_degree[course] -= 1
                    if in_degree[course] == 0:
                        queue.append(course)

        if len(topo_order) != len(self.courses):
            raise ValueError("Cannot create valid ordering - check prerequisites")

        return topo_order

    def can_take_course(self, course_code: str, completed: Set[str]) -> bool:
        """Check if a course can be taken given completed courses."""
        if course_code not in self.courses:
            return False
        prerequisites = self.graph[course_code]
        return prerequisites.issubset(completed)

    def get_available_courses(self, completed: Set[str]) -> List[str]:
        """Get all courses that can be taken given completed courses."""
        return [code for code in self.courses
                if self.can_take_course(code, completed) and code not in completed]
