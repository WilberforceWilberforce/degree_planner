from typing import List, Set, Dict
from .course import Course
from .dag import DAG
from .workload_predictor import WorkloadPredictor


class DegreeScheduler:
    """Generates balanced 4-year degree plans using greedy scheduling."""

    def __init__(self, courses: List[Course]):
        self.courses = {course.code: course for course in courses}
        self.dag = DAG(courses)
        self.predictor = WorkloadPredictor()
        self.predictor.train(courses)

    def schedule(self, target_credits_per_semester: float = 15.0,
                num_semesters: int = 8) -> List[List[Course]]:
        """
        Generate a balanced schedule using greedy algorithm.

        Args:
            target_credits_per_semester: Target credits per semester
            num_semesters: Number of semesters (typically 8 for 4 years)

        Returns:
            List of semesters, each containing scheduled courses
        """
        schedule = [[] for _ in range(num_semesters)]
        completed = set()
        semester_credits = [0] * num_semesters

        for semester in range(num_semesters):
            # Get available courses
            available = self.dag.get_available_courses(completed)
            available_courses = [self.courses[code] for code in available]

            # Sort by difficulty (greedy: take easier courses first when possible)
            available_courses.sort(
                key=lambda c: (self.predictor.predict_difficulty(c), c.credits)
            )

            # Greedily add courses to this semester
            for course in available_courses:
                remaining_capacity = target_credits_per_semester - semester_credits[semester]

                if course.credits <= remaining_capacity:
                    schedule[semester].append(course)
                    semester_credits[semester] += course.credits
                    completed.add(course.code)

        # Validate schedule
        if len(completed) != len(self.courses):
            raise ValueError("Could not schedule all courses")

        return schedule

    def get_schedule_summary(self, schedule: List[List[Course]]) -> str:
        """Generate a human-readable schedule summary."""
        summary = []
        summary.append("=" * 80)
        summary.append("PERSONALIZED 4-YEAR DEGREE PLAN")
        summary.append("=" * 80)
        summary.append("")

        total_credits = 0
        for semester_idx, courses in enumerate(schedule):
            year = (semester_idx // 2) + 1
            semester_type = "Fall" if semester_idx % 2 == 0 else "Spring"
            semester_credits = sum(c.credits for c in courses)
            total_credits += semester_credits

            summary.append(f"YEAR {year} - {semester_type} Semester")
            summary.append("-" * 80)

            if courses:
                for course in courses:
                    difficulty = self.predictor.predict_difficulty(course)
                    summary.append(f"  {course.code:10} | {course.name:30} | "
                                 f"Credits: {course.credits} | Difficulty: {difficulty:.1f}/5.0")
            else:
                summary.append("  (No courses scheduled)")

            summary.append(f"  Semester Total: {semester_credits} credits")
            summary.append("")

        summary.append("=" * 80)
        summary.append(f"TOTAL CREDITS: {total_credits}")
        summary.append("=" * 80)

        return "\n".join(summary)
