import sqlite3

class Database:
    def __init__(self, database_name="student_management.db"):
        self.database_name = database_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database_name)
            self.connection.execute("PRAGMA foreign_keys = ON")
            return self.connection
        except sqlite3.Error as error:
            raise RuntimeError(f"Database connection failed: {error}") from error

    def create_table(self):
        if self.connection is None:
            self.connect()
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK (age > 0),
            course TEXT NOT NULL,
            marks REAL NOT NULL CHECK (marks >= 0 AND marks <= 100)
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
        query = """INSERT INTO students (student_id, name, age, course, marks)
                    VALUES (?, ?, ?, ?, ?)"""
        values = (student.student_id, student.name.strip(), student.age,
                  student.course.strip(), student.marks)
        try:
            self.connection.execute(query, values)
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as error:
            self.connection.rollback()
            message = str(error).lower()
            if "unique constraint" in message or "primary key" in message:
                raise ValueError("Student ID already exists.") from error
            raise ValueError(f"Database constraint failed: {error}") from error
        except sqlite3.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Could not insert student: {error}") from error

    def get_all_students(self):
        query = """SELECT student_id, name, age, course, marks
                    FROM students ORDER BY student_id"""
        try:
            return self.connection.execute(query).fetchall()
        except sqlite3.Error as error:
            raise RuntimeError(f"Could not retrieve students: {error}") from error

    def get_student_by_id(self, student_id):
        query = """SELECT student_id, name, age, course, marks
                   FROM students WHERE student_id = ?"""
        try:
            return self.connection.execute(query, (student_id,)).fetchone()
        except sqlite3.Error as error:
            raise RuntimeError(f"Could not search student: {error}") from error

    def update_student(self, student):
        # Validate every changed value before attempting the UPDATE.
        student.validate()
        query = """UPDATE students
                   SET name = ?, age = ?, course = ?, marks = ?
                   WHERE student_id = ?"""
        values = (student.name.strip(), student.age, student.course.strip(),
                  student.marks, student.student_id)
        try:
            cursor = self.connection.execute(query, values)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.IntegrityError as error:
            self.connection.rollback()
            raise ValueError(f"Update rejected by database constraints: {error}") from error
        except sqlite3.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Could not update student: {error}") from error

    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE student_id = ?"
        try:
            cursor = self.connection.execute(query, (student_id,))
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Could not delete student: {error}") from error

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
