"""
database.py  -  SQL-PY-007: Database Transactions & ACID

All database work lives here. The key idea of this task:
transfer_student_course() wraps TWO SQL statements in ONE transaction,
so either both are saved (COMMIT) or none are (ROLLBACK).
"""
import sqlite3


class Database:
    def __init__(self, db_name="student_management.db"):
        self.db_name = db_name
        # isolation_level=None -> Python does NOT start transactions silently.
        # We control BEGIN / COMMIT / ROLLBACK ourselves (explicit boundaries).
        self.conn = sqlite3.connect(db_name, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
        self.create_tables()
        self.create_history_table()

    # ------------------------------------------------------------------
    # Transaction control  (NEW in SQL-PY-007)
    # ------------------------------------------------------------------
    def begin_transaction(self):
        """Start a transaction: changes are temporary until commit()."""
        self.conn.execute("BEGIN")

    def commit(self):
        """Make every change since BEGIN permanent."""
        if self.conn.in_transaction:
            self.conn.commit()

    def rollback(self):
        """Cancel every uncommitted change since BEGIN."""
        if self.conn.in_transaction:
            self.conn.rollback()

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name    TEXT NOT NULL UNIQUE,
                duration_years INTEGER NOT NULL DEFAULT 3
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                age        INTEGER NOT NULL CHECK (age BETWEEN 15 AND 60),
                email      TEXT NOT NULL UNIQUE,
                marks      REAL NOT NULL CHECK (marks BETWEEN 0 AND 100),
                course_id  INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )""")

    def create_history_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS student_course_history (
                history_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id    INTEGER NOT NULL,
                old_course_id INTEGER NOT NULL,
                new_course_id INTEGER NOT NULL,
                changed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id)    REFERENCES students(student_id),
                FOREIGN KEY (old_course_id) REFERENCES courses(course_id),
                FOREIGN KEY (new_course_id) REFERENCES courses(course_id)
            )""")

    def seed_sample_data(self):
        """Insert demo data only when the database is empty."""
        if self.conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0] > 0:
            return False
        for name, years in [("BCA", 3), ("MCA", 2), ("BBA", 3), ("BSC", 3), ("MBA", 2)]:
            self.conn.execute(
                "INSERT INTO courses (course_name, duration_years) VALUES (?, ?)", (name, years))
        students = [
            ("Rahul", 20, "rahul@example.com", 78.5, 1),
            ("Priya", 21, "priya@example.com", 91.0, 1),
            ("Amit", 22, "amit@example.com", 64.0, 3),
            ("Sneha", 20, "sneha@example.com", 85.5, 4),
            ("Karan", 23, "karan@example.com", 72.0, 2),
            ("Neha", 21, "neha@example.com", 88.0, 3),
        ]
        for s in students:
            self.conn.execute(
                "INSERT INTO students (name, age, email, marks, course_id) VALUES (?,?,?,?,?)", s)
        return True

    # ------------------------------------------------------------------
    # Courses  (SQL-PY-006)
    # ------------------------------------------------------------------
    def add_course(self, course):
        ok, msg = course.validate()
        if not ok:
            return False, msg
        try:
            self.conn.execute(
                "INSERT INTO courses (course_name, duration_years) VALUES (?, ?)",
                (course.course_name, course.duration_years))
            return True, f"Course {course.course_name} added."
        except sqlite3.IntegrityError:
            return False, f"Course {course.course_name} already exists."

    def get_all_courses(self):
        return self.conn.execute("SELECT * FROM courses ORDER BY course_id").fetchall()

    def get_course_by_id(self, course_id):
        return self.conn.execute(
            "SELECT * FROM courses WHERE course_id = ?", (course_id,)).fetchone()

    def get_courses_without_students(self):
        return self.conn.execute("""
            SELECT c.course_id, c.course_name
            FROM courses c LEFT JOIN students s ON s.course_id = c.course_id
            WHERE s.student_id IS NULL ORDER BY c.course_id""").fetchall()

    # ------------------------------------------------------------------
    # Students: CRUD  (SQL-PY-003)
    # ------------------------------------------------------------------
    _STUDENT_SELECT = """
        SELECT s.student_id, s.name, s.age, s.email, s.marks,
               s.course_id, c.course_name
        FROM students s LEFT JOIN courses c ON s.course_id = c.course_id """

    def add_student(self, student):
        ok, msg = student.validate()
        if not ok:
            return False, msg
        if self.get_course_by_id(student.course_id) is None:
            return False, "Course does not exist."
        try:
            self.conn.execute(
                "INSERT INTO students (name, age, email, marks, course_id) VALUES (?,?,?,?,?)",
                (student.name, student.age, student.email, student.marks, student.course_id))
            return True, "Student added."
        except sqlite3.IntegrityError as e:
            return False, f"Could not add student: {e}"

    def get_all_students(self):
        return self.conn.execute(self._STUDENT_SELECT + "ORDER BY s.student_id").fetchall()

    def get_student_by_id(self, student_id):
        return self.conn.execute(
            self._STUDENT_SELECT + "WHERE s.student_id = ?", (student_id,)).fetchone()

    def update_student(self, student_id, name, age, email, marks):
        if self.get_student_by_id(student_id) is None:
            return False, "Student not found."
        try:
            self.conn.execute(
                "UPDATE students SET name=?, age=?, email=?, marks=? WHERE student_id=?",
                (name, age, email, marks, student_id))
            return True, "Student updated."
        except sqlite3.IntegrityError as e:
            return False, f"Could not update student: {e}"

    def delete_student(self, student_id):
        """Delete history + student together, as ONE transaction."""
        if self.get_student_by_id(student_id) is None:
            return False, "Student not found."
        try:
            self.begin_transaction()
            self.conn.execute(
                "DELETE FROM student_course_history WHERE student_id = ?", (student_id,))
            self.conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.commit()
            return True, "Student deleted."
        except sqlite3.Error as e:
            self.rollback()
            return False, f"Delete failed, rolled back: {e}"

    # ------------------------------------------------------------------
    # Search / filter / sort  (SQL-PY-004)
    # ------------------------------------------------------------------
    def search_student_by_name(self, keyword):
        return self.conn.execute(
            self._STUDENT_SELECT + "WHERE s.name LIKE ? ORDER BY s.name",
            (f"%{keyword}%",)).fetchall()

    def search_students_by_course(self, course_name):
        return self.conn.execute(
            self._STUDENT_SELECT + "WHERE c.course_name = ? ORDER BY s.name",
            (course_name.strip().upper(),)).fetchall()

    def search_students_by_marks(self, min_marks, max_marks=100):
        return self.conn.execute(
            self._STUDENT_SELECT + "WHERE s.marks BETWEEN ? AND ? ORDER BY s.marks DESC",
            (min_marks, max_marks)).fetchall()

    def sort_students(self, column="name", descending=False):
        allowed = {"name", "age", "marks", "student_id"}   # whitelist -> no SQL injection
        if column not in allowed:
            column = "name"
        order = "DESC" if descending else "ASC"
        return self.conn.execute(
            self._STUDENT_SELECT + f"ORDER BY s.{column} {order}").fetchall()

    def get_top_students(self, n):
        return self.conn.execute(
            self._STUDENT_SELECT + "ORDER BY s.marks DESC LIMIT ?", (n,)).fetchall()

    # ------------------------------------------------------------------
    # Aggregation  (SQL-PY-005)
    # ------------------------------------------------------------------
    def get_student_statistics(self):
        return self.conn.execute("""
            SELECT COUNT(*) AS total, ROUND(AVG(marks),2) AS average,
                   MAX(marks) AS highest, MIN(marks) AS lowest
            FROM students""").fetchone()

    def get_course_statistics(self):
        return self.conn.execute("""
            SELECT c.course_name, COUNT(s.student_id) AS total_students,
                   ROUND(AVG(s.marks),2) AS average_marks
            FROM courses c LEFT JOIN students s ON s.course_id = c.course_id
            GROUP BY c.course_id ORDER BY c.course_name""").fetchall()

    # ------------------------------------------------------------------
    # Course transfer  (NEW in SQL-PY-007)
    # ------------------------------------------------------------------
    def transfer_student_course(self, student_id, new_course_id, simulate_failure=False):
        """
        Move a student to another course.  Returns (success: bool, message: str).

        Step 1 - VALIDATE first (no transaction yet, nothing can change).
        Step 2 - BEGIN a transaction.
        Step 3 - UPDATE students            }  both must succeed
        Step 4 - INSERT history             }  together
        Step 5 - COMMIT  (or ROLLBACK if anything raised)

        simulate_failure=True raises an error AFTER the update and BEFORE the
        history insert, to demonstrate Atomicity (Test 5).
        """
        # ---- Step 1: validation ----
        student = self.get_student_by_id(student_id)
        if student is None:
            return False, f"Student ID {student_id} does not exist."
        new_course = self.get_course_by_id(new_course_id)
        if new_course is None:
            return False, f"Course ID {new_course_id} does not exist."
        old_course_id = student["course_id"]
        if old_course_id is None:
            return False, f"{student['name']} is not enrolled in any course yet."
        if old_course_id == new_course_id:
            return False, f"{student['name']} is already enrolled in {new_course['course_name']}."

        old_course_name = student["course_name"]

        # ---- Steps 2-5: one transaction ----
        try:
            self.begin_transaction()
            self.conn.execute(
                "UPDATE students SET course_id = ? WHERE student_id = ?",
                (new_course_id, student_id))

            if simulate_failure:
                raise RuntimeError("Simulated failure before inserting history")

            self.conn.execute(
                "INSERT INTO student_course_history "
                "(student_id, old_course_id, new_course_id) VALUES (?, ?, ?)",
                (student_id, old_course_id, new_course_id))
            self.commit()
            return True, (f"{student['name']} transferred from {old_course_name} "
                          f"to {new_course['course_name']}. Transaction committed.")
        except Exception as e:
            self.rollback()   # undo the UPDATE -> no partial change
            return False, f"Transfer failed ({e}). Transaction rolled back; no changes saved."

    def get_course_history(self):
        """Full transfer history of all students."""
        return self.conn.execute(self._HISTORY_SELECT + "ORDER BY h.history_id").fetchall()

    def get_student_course_history(self, student_id):
        """Transfer history of one student."""
        return self.conn.execute(
            self._HISTORY_SELECT + "WHERE h.student_id = ? ORDER BY h.history_id",
            (student_id,)).fetchall()

    _HISTORY_SELECT = """
        SELECT h.history_id, s.name AS student_name,
               oc.course_name AS old_course, nc.course_name AS new_course,
               h.changed_at
        FROM student_course_history h
        JOIN students s  ON s.student_id  = h.student_id
        JOIN courses  oc ON oc.course_id  = h.old_course_id
        JOIN courses  nc ON nc.course_id  = h.new_course_id """

    def close(self):
        self.rollback()
        self.conn.close()
