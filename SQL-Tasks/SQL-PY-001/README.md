# SQL-PY-001 — Python–SQL Database Foundation

## Problem statement
Build a University Student Management System that stores student records permanently in SQLite instead of keeping them only in a Python list.

## Technologies
- Python
- SQLite
- Python's built-in `sqlite3` module

## Project files
- `main.py` — menu and application flow
- `student.py` — Student class and input validation
- `database.py` — SQLite connection, table creation, INSERT and SELECT queries
- `student_management.db` — created automatically when the program runs
- `README.md` — project explanation and run instructions

## Database table
The `students` table contains:
| Column | SQLite type | Description |
|---|---|---|
| student_id | INTEGER | Student identifier |
| name | TEXT | Student name |
| age | INTEGER | Student age |
| course | TEXT | Course name |
| marks | REAL | Marks from 0 to 100 |

## SQL concepts used
- `CREATE TABLE IF NOT EXISTS` creates the table if it does not already exist.
- `INSERT INTO` stores a student record.
- `SELECT` retrieves student records.
- `WHERE` searches for a student by ID.
- `?` placeholders are parameterized SQL; values are supplied separately.

## Validation
- Student ID must be an integer.
- Name cannot be empty.
- Age must be an integer greater than 0.
- Course cannot be empty.
- Marks must be between 0 and 100.

## How Python communicates with SQL
1. `sqlite3.connect()` opens or creates the database file.
2. `connection.cursor()` creates a cursor to execute SQL.
3. `cursor.execute()` runs an SQL statement.
4. `commit()` saves an insertion permanently.
5. `fetchall()` retrieves all matching rows; `fetchone()` retrieves one.
6. `close()` closes the database connection.

## Run the project
Open Terminal in this project folder and run:

```bash
python3 main.py
```

No separate SQLite installation or pip package is required; `sqlite3` is included with standard Python installations.

## Test checklist
- Add a valid student.
- View all students.
- Search for an existing student ID.
- Search for a non-existing ID and verify `Student not found`.
- Try a negative age.
- Try marks above 100.
- Try an empty name.

## Sample data from the task
The task document lists:
1. Rahul, 20, BCA, 82
2. Priya, 21, BCA, 88
3. Amit, 20, BBA, 76
4. Neha, 22, BCA, 91
5. Rohit, 21, BBA, 69

You can enter these records through the Add Student menu.
