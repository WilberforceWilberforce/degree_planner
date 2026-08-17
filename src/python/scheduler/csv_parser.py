import csv
from typing import List
from .course import Course


class CSVParser:
    """Parses course data from CSV files."""

    @staticmethod
    def parse_courses(filepath: str) -> List[Course]:
        """
        Parse courses from a CSV file.

        Expected columns:
        - course_code: Unique course identifier
        - course_name: Human-readable course name
        - credits: Number of credit hours
        - prerequisites: Semicolon-separated list of prerequisite codes
        - difficulty: Estimated difficulty (1-5 scale)
        """
        courses = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                if reader.fieldnames is None:
                    raise ValueError("CSV file is empty")

                required_fields = {'course_code', 'course_name', 'credits'}
                if not required_fields.issubset(set(reader.fieldnames)):
                    raise ValueError(f"Missing required fields. Required: {required_fields}")

                for row_num, row in enumerate(reader, start=2):
                    try:
                        course = Course.from_dict(row)
                        courses.append(course)
                    except (KeyError, ValueError) as e:
                        raise ValueError(f"Error parsing row {row_num}: {e}")

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        if not courses:
            raise ValueError("No courses found in CSV file")

        return courses
