class Student:
    def __init__(self, student_id, name, age, course_id, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course_id = course_id
        self.marks = marks

    def validate(self):
        if not isinstance(self.student_id, int):
            raise ValueError("Student ID must be an integer.")
        if not self.name.strip():
            raise ValueError("Name cannot be empty.")
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be a positive integer.")
        if not isinstance(self.course_id, int):
            raise ValueError("Course ID must be an integer.")
        if not 0 <= float(self.marks) <= 100:
            raise ValueError("Marks must be between 0 and 100.")
        return True

    def to_tuple(self):
        self.validate()
        return (self.student_id, self.name.strip(), self.age,
                self.course_id, float(self.marks))
