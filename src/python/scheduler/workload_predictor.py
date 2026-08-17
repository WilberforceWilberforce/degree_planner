import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple
from .course import Course


class WorkloadPredictor:
    """Predicts course difficulty using machine learning."""

    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.trained = False

    def train(self, courses: List[Course]) -> None:
        """Train the workload prediction model."""
        if len(courses) < 2:
            self.trained = False
            return

        X = np.array([[len(course.prerequisites), course.credits]
                      for course in courses]).reshape(-1, 2)
        y = np.array([course.difficulty for course in courses])

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.trained = True

    def predict_difficulty(self, course: Course) -> float:
        """Predict difficulty for a course."""
        if not self.trained:
            return course.difficulty

        features = np.array([[len(course.prerequisites), course.credits]]).reshape(1, -2)
        features_scaled = self.scaler.transform(features)
        predicted = self.model.predict(features_scaled)[0]
        return float(np.clip(predicted, 1.0, 5.0))

    def get_courses_by_difficulty(self, courses: List[Course],
                                   target_credits: int,
                                   max_difficulty: float) -> List[Course]:
        """Get courses that fit within difficulty and credit constraints."""
        available = [c for c in courses
                    if c.credits <= target_credits
                    and self.predict_difficulty(c) <= max_difficulty]
        return sorted(available, key=lambda c: self.predict_difficulty(c))
