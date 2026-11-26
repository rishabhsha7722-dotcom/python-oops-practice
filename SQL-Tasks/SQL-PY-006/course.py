class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def validate(self):
        if not isinstance(self.course_id, int):
            raise ValueError("Course ID must be an integer.")
        if not self.course_name.strip():
            raise ValueError("Course name cannot be empty.")
        return True

    def to_tuple(self):
        self.validate()
        return (self.course_id, self.course_name.strip())
