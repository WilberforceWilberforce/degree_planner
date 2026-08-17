from dataclasses import dataclass
from typing import Set, List


@dataclass
class Course:
    """Represents a course with its properties."""
    code: str
    name: str
    credits: int
    prerequisites: Set[str]
    difficulty: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Course':
        """Create a Course from a dictionary."""
        prereqs = set()
        if isinstance(data.get('prerequisites'), str) and data['prerequisites']:
            prereqs = set(code.strip() for code in data['prerequisites'].split(';'))

        return cls(
            code=data['course_code'],
            name=data['course_name'],
            credits=int(data['credits']),
            prerequisites=prereqs,
            difficulty=float(data.get('difficulty', 1.0))
        )

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.code == other.code
        return False
