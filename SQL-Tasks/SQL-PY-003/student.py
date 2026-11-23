class Student:
    """Student model and input validation."""
    def __init__(self, student_id, name, age, course, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def validate(self):
        if not isinstance(self.student_id, int):
            raise ValueError("Student ID must be an integer.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Student name cannot be empty.")
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be an integer greater than 0.")
        if not isinstance(self.course, str) or not self.course.strip():
            raise ValueError("Course cannot be empty.")
        if not isinstance(self.marks, (int, float)) or not 0 <= self.marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")
        return True
