import sqlite3
from student import Student
from course import Course


class Database:
    def __init__(self, db_name="student_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_course_table()
        self.create_student_table()

    def create_course_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL UNIQUE
            )
        """)
        self.conn.commit()

    def create_student_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course_id INTEGER NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        """)
        self.conn.commit()

    # Course CRUD
    def add_course(self, course):
        if isinstance(course, Course):
            values = course.to_tuple()
        else:
            values = Course(*course).to_tuple()
        self.cursor.execute(
            "INSERT INTO courses (course_id, course_name) VALUES (?, ?)", values
        )
        self.conn.commit()

    def get_all_courses(self):
        self.cursor.execute("SELECT course_id, course_name FROM courses ORDER BY course_id")
        return self.cursor.fetchall()

    def get_course_by_id(self, course_id):
        self.cursor.execute(
            "SELECT course_id, course_name FROM courses WHERE course_id = ?", (course_id,)
        )
        return self.cursor.fetchone()

    def delete_course(self, course_id):
        # Foreign-key restriction prevents deleting a course still used by students.
        self.cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
        self.conn.commit()
        return self.cursor.rowcount

    # Student CRUD
    def add_student(self, student):
        values = student.to_tuple() if isinstance(student, Student) else Student(*student).to_tuple()
        if self.get_course_by_id(values[3]) is None:
            raise ValueError("Invalid course ID.")
        self.cursor.execute("""
            INSERT INTO students (student_id, name, age, course_id, marks)
            VALUES (?, ?, ?, ?, ?)
        """, values)
        self.conn.commit()

    def get_all_students(self):
        return self.get_students_with_courses()

    def get_student_by_id(self, student_id):
        self.cursor.execute("""
            SELECT s.student_id, s.name, s.age, s.course_id, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.student_id = ?
        """, (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id, student):
        values = student.to_tuple() if isinstance(student, Student) else Student(*student).to_tuple()
        if self.get_course_by_id(values[3]) is None:
            raise ValueError("Invalid course ID.")
        self.cursor.execute("""
            UPDATE students SET name = ?, age = ?, course_id = ?, marks = ?
            WHERE student_id = ?
        """, (values[1], values[2], values[3], values[4], student_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()
        return self.cursor.rowcount

    # Join/filter/sort/top features carried forward
    def get_students_with_courses(self):
        self.cursor.execute("""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY s.student_id
        """)
        return self.cursor.fetchall()

    def get_students_by_course(self, course_name):
        self.cursor.execute("""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s
            INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE c.course_name = ?
            ORDER BY s.name
        """, (course_name,))
        return self.cursor.fetchall()

    def get_students_by_marks(self, min_marks):
        self.cursor.execute("""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.marks >= ? ORDER BY s.marks DESC
        """, (min_marks,))
        return self.cursor.fetchall()

    def search_students_by_name(self, keyword):
        self.cursor.execute("""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s INNER JOIN courses AS c ON s.course_id = c.course_id
            WHERE s.name LIKE ? ORDER BY s.name
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def get_students_sorted_by_marks(self, desc=True):
        direction = "DESC" if desc else "ASC"
        self.cursor.execute(f"""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY s.marks {direction}
        """)
        return self.cursor.fetchall()

    def get_top_students(self, limit):
        self.cursor.execute("""
            SELECT s.student_id, s.name, c.course_name, s.marks
            FROM students AS s INNER JOIN courses AS c ON s.course_id = c.course_id
            ORDER BY s.marks DESC LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    # Analytics carried forward, using JOIN/GROUP BY
    def get_total_students(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        return self.cursor.fetchone()[0]

    def get_average_marks(self):
        self.cursor.execute("SELECT AVG(marks) FROM students")
        return self.cursor.fetchone()[0] or 0

    def get_total_marks(self):
        self.cursor.execute("SELECT SUM(marks) FROM students")
        return self.cursor.fetchone()[0] or 0

    def get_highest_marks(self):
        self.cursor.execute("SELECT MAX(marks) FROM students")
        return self.cursor.fetchone()[0] or 0

    def get_lowest_marks(self):
        self.cursor.execute("SELECT MIN(marks) FROM students")
        return self.cursor.fetchone()[0] or 0

    def get_course_statistics(self):
        self.cursor.execute("""
            SELECT c.course_name, COUNT(s.student_id), AVG(s.marks),
                   MAX(s.marks), MIN(s.marks)
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
        """)
        return self.cursor.fetchall()

    def get_course_average_marks(self):
        self.cursor.execute("""
            SELECT c.course_name, AVG(s.marks)
            FROM courses AS c LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
        """)
        return self.cursor.fetchall()

    def get_course_highest_marks(self):
        self.cursor.execute("""
            SELECT c.course_name, MAX(s.marks)
            FROM courses AS c LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
        """)
        return self.cursor.fetchall()

    def get_course_lowest_marks(self):
        self.cursor.execute("""
            SELECT c.course_name, MIN(s.marks)
            FROM courses AS c LEFT JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
        """)
        return self.cursor.fetchall()

    def get_courses_above_average(self, min_average):
        self.cursor.execute("""
            SELECT c.course_name, AVG(s.marks)
            FROM courses AS c INNER JOIN students AS s ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            HAVING AVG(s.marks) >= ?
            ORDER BY AVG(s.marks) DESC
        """, (min_average,))
        return self.cursor.fetchall()

    def get_courses_without_students(self):
        self.cursor.execute("""
            SELECT c.course_name
            FROM courses AS c
            LEFT JOIN students AS s ON c.course_id = s.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
