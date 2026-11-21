import sqlite3
from student import Student


class Database:
    """Handles SQLite connection and student database operations."""

    def __init__(self, database_name="student_management.db"):
        self.database_name = database_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database_name)
            # Makes SQLite enforce foreign keys if we add them in later tasks.
            self.connection.execute("PRAGMA foreign_keys = ON")
            return self.connection
        except sqlite3.Error as error:
            raise RuntimeError(f"Database connection failed: {error}") from error

    def create_table(self):
        if self.connection is None:
            self.connect()

        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER,
            name TEXT,
            age INTEGER,
            course TEXT,
            marks REAL
        )
        """
        try:
            self.connection.execute(query)
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Could not create students table: {error}") from error

    def add_student(self, student):
        student.validate()

        query = """
        INSERT INTO students (student_id, name, age, course, marks)
        VALUES (?, ?, ?, ?, ?)
        """
        values = (
            student.student_id,
            student.name.strip(),
            student.age,
            student.course.strip(),
            student.marks,
        )

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Could not insert student: {error}") from error

    def get_all_students(self):
        query = "SELECT student_id, name, age, course, marks FROM students ORDER BY student_id"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as error:
            raise RuntimeError(f"Could not retrieve students: {error}") from error

    def get_student_by_id(self, student_id):
        query = """
        SELECT student_id, name, age, course, marks
        FROM students
        WHERE student_id = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
        except sqlite3.Error as error:
            raise RuntimeError(f"Could not search student: {error}") from error

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
