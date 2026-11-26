"""Student model for the Student Management System."""


class Student:
    def __init__(self, name, age, email, marks, course_id, student_id=None):
        self.student_id = student_id
        self.name = name.strip()
        self.age = age
        self.email = email.strip().lower()
        self.marks = marks
        self.course_id = course_id

    def validate(self):
        if not self.name:
            return False, "Name cannot be empty."
        if not (15 <= self.age <= 60):
            return False, "Age must be between 15 and 60."
        if "@" not in self.email or "." not in self.email:
            return False, "Email is not valid."
        if not (0 <= self.marks <= 100):
            return False, "Marks must be between 0 and 100."
        return True, "OK"

    def __str__(self):
        return f"[{self.student_id}] {self.name} | {self.age} | {self.email} | {self.marks}"
