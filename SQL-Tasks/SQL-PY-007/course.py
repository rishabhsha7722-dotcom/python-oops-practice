"""Course model for the Student Management System."""


class Course:
    def __init__(self, course_name, duration_years=3, course_id=None):
        self.course_id = course_id
        self.course_name = course_name.strip().upper()
        self.duration_years = duration_years

    def validate(self):
        if not self.course_name:
            return False, "Course name cannot be empty."
        if not isinstance(self.duration_years, int) or not (1 <= self.duration_years <= 6):
            return False, "Duration must be a whole number between 1 and 6 years."
        return True, "OK"

    def __str__(self):
        return f"[{self.course_id}] {self.course_name} ({self.duration_years} yrs)"
