# SQL-PY-002 — Robust Student Database with Constraints

## Objective
Upgrade SQL-PY-001 using database constraints while continuing the same Student Management System.

## Technologies
Python, SQLite (`sqlite3` built into Python), SQL, OOP.

## Files
- `main.py`: menu/application flow
- `student.py`: Student class and Python validation
- `database.py`: SQLite, constrained table, INSERT and SELECT/WHERE
- `student_management.db`: created when the program runs
- `README.md`: documentation

## Table design
```sql
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0),
    course TEXT NOT NULL,
    marks REAL NOT NULL CHECK (marks >= 0 AND marks <= 100)
);
```

## Concepts
- `PRIMARY KEY`: uniquely identifies each student; duplicate IDs are rejected.
- `NOT NULL`: required columns cannot contain NULL.
- `CHECK`: database enforces age > 0 and marks from 0 to 100.
- Python validation gives clear messages before SQL; database constraints protect stored data independently.

## Run
```bash
python3 main.py
```

## Important migration note
SQLite does not retrofit constraints onto an existing table using `CREATE TABLE IF NOT EXISTS`. Back up your Task 1 database first. For this introductory task, close the app and rename or remove the old `student_management.db`, then run this version to create the constrained schema. Re-enter records, or use a deliberate table migration if you need to preserve them.

## Required tests
1. Add ID 6, Karan, 20, BCA, 85 — success.
2. Insert an existing ID — `Student ID already exists.`
3. Age -5 — validation error.
4. Marks 150 — validation error.
5. Empty name — error.
6. Empty course — error.
7. Search existing ID — matching row.
8. Search missing ID — `Student not found.`

## Example SQL
Parameterized insert:
```sql
INSERT INTO students (student_id, name, age, course, marks)
VALUES (?, ?, ?, ?, ?);
```
Search:
```sql
SELECT student_id, name, age, course, marks
FROM students
WHERE student_id = ?;
```

## Viva answers
- Primary key: value(s) uniquely identifying a row.
- NOT NULL: a column must have a value, not NULL.
- CHECK: rule required for a stored value.
- Duplicate primary key: SQLite rejects the insert; the app handles the error.
- NULL is missing/unknown; empty string is text containing zero characters.
- Python validation and database constraints are both useful: app-friendly feedback plus storage-level protection.
- DEFAULT supplies a value if a column is omitted; optional challenge for this task.
