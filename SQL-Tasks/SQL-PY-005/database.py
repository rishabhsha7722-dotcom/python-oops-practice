import sqlite3


class Database:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER CHECK (age > 0),
                course TEXT NOT NULL,
                marks REAL CHECK (marks >= 0 AND marks <= 100)
            )
        """)
        self.conn.commit()

    # SQL-PY-001 to SQL-PY-004: existing CRUD
    def add_student(self, student):
        self.cursor.execute(
            "INSERT INTO students (student_id, name, age, course, marks) VALUES (?, ?, ?, ?, ?)",
            (student["student_id"], student["name"], student["age"],
             student["course"], student["marks"])
        )
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id, student):
        self.cursor.execute("""
            UPDATE students SET name = ?, age = ?, course = ?, marks = ?
            WHERE student_id = ?
        """, (student["name"], student["age"], student["course"],
              student["marks"], student_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()
        return self.cursor.rowcount

    # SQL-PY-004: filtering and sorting
    def get_students_by_course(self, course):
        self.cursor.execute("SELECT * FROM students WHERE course = ?", (course,))
        return self.cursor.fetchall()

    def get_students_by_marks(self, min_marks):
        self.cursor.execute("SELECT * FROM students WHERE marks >= ?", (min_marks,))
        return self.cursor.fetchall()

    def search_students_by_name(self, keyword):
        pattern = f"%{keyword}%"
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ?", (pattern,))
        return self.cursor.fetchall()

    def get_students_sorted_by_marks(self, desc=True):
        order = "DESC" if desc else "ASC"
        self.cursor.execute(f"SELECT * FROM students ORDER BY marks {order}")
        return self.cursor.fetchall()

    def get_top_students(self, limit):
        self.cursor.execute(
            "SELECT * FROM students ORDER BY marks DESC LIMIT ?", (limit,)
        )
        return self.cursor.fetchall()

    # SQL-PY-005: single-student-table analytics (computed in SQL)
    def get_total_students(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        return self.cursor.fetchone()[0]

    def get_average_marks(self):
        self.cursor.execute("SELECT AVG(marks) FROM students")
        value = self.cursor.fetchone()[0]
        return value if value is not None else 0

    def get_total_marks(self):
        self.cursor.execute("SELECT SUM(marks) FROM students")
        value = self.cursor.fetchone()[0]
        return value if value is not None else 0

    def get_highest_marks(self):
        self.cursor.execute("SELECT MAX(marks) FROM students")
        value = self.cursor.fetchone()[0]
        return value if value is not None else 0

    def get_lowest_marks(self):
        self.cursor.execute("SELECT MIN(marks) FROM students")
        value = self.cursor.fetchone()[0]
        return value if value is not None else 0

    def get_course_statistics(self):
        self.cursor.execute("""
            SELECT course, COUNT(*) AS total_students,
                   AVG(marks) AS average_marks,
                   MAX(marks) AS highest_marks,
                   MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
            ORDER BY course ASC
        """)
        return self.cursor.fetchall()

    def get_course_average_marks(self):
        self.cursor.execute("""
            SELECT course, AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            ORDER BY course ASC
        """)
        return self.cursor.fetchall()

    def get_course_highest_marks(self):
        self.cursor.execute("""
            SELECT course, MAX(marks) AS highest_marks
            FROM students
            GROUP BY course
            ORDER BY course ASC
        """)
        return self.cursor.fetchall()

    def get_course_lowest_marks(self):
        self.cursor.execute("""
            SELECT course, MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
            ORDER BY course ASC
        """)
        return self.cursor.fetchall()

    def get_courses_above_average(self, min_average):
        self.cursor.execute("""
            SELECT course, AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            HAVING AVG(marks) >= ?
            ORDER BY average_marks DESC
        """, (min_average,))
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
