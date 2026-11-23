# SQL-PY-003 — Student CRUD Operations

## Objective
Continue the Student Management System from SQL-PY-002 and implement Create, Read, Update and Delete (CRUD).

## Project files
- `main.py`: six-option user menu and interaction
- `student.py`: Student class and Python validation
- `database.py`: SQLite connection, constraints, INSERT/SELECT/UPDATE/DELETE
- `student_management.db`: created automatically
- `README.md`: documentation

## Table schema
The Task 2 constraints are retained:
```sql
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK(age > 0),
    course TEXT NOT NULL,
    marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
);
```

## CRUD operations
- Create: `INSERT INTO`
- Read: `SELECT`, including `SELECT ... WHERE student_id = ?`
- Update: `UPDATE ... SET ... WHERE student_id = ?`
- Delete: `DELETE ... WHERE student_id = ?`

The primary key is not changed by UPDATE. Parameter placeholders (`?`) are used throughout.

## New concepts
- `cursor.rowcount`: number of rows changed. 0 means no matching ID; normally 1 means one student changed.
- Delete confirmation: the student is shown first; deletion happens only if the user types `yes`.
- `commit()`: save a successful database operation.
- `rollback()`: cancel the current transaction after an operation fails.

## Run
```bash
python3 main.py
```

## Assignment test plan
1. Add ID 6, Karan, 20, BCA, 85.
2. View all and confirm ID 6 appears.
3. Search ID 3 and check Amit, 20, BBA, 76 (if the Task 1 sample records were entered).
4. Update ID 3 marks to 90.
5. Attempt marks 150; validation should reject it and data should remain unchanged.
6. Delete ID 6 and type `yes`.
7. Delete/search ID 100; expect `Student not found.`
8. Try deleting an existing student and type `no`; expect `Deletion cancelled.` and record remains.

## Safety
Never omit `WHERE` from UPDATE or DELETE: without it, every row could be modified or removed. Always use parameterized SQL.

## Viva quick answers
- CRUD = Create, Read, Update, Delete.
- INSERT adds a new row; UPDATE modifies existing row(s).
- DELETE removes rows; DROP removes a database object such as a table.
- WHERE limits which rows a query affects.
- `rowcount` reports affected rows.
- `student_id` is the primary key and should remain stable.
- Validate updated values just like new values.
- Ask confirmation before deleting to prevent accidental loss.
