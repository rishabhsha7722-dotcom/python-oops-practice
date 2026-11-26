# SQL-PY-006 — Student Database Relationships & JOINs

Continues SQL-PY-005 and adds a separate `courses` table related to `students` by a foreign key.

## Project files (required)
- `main.py` — 15-option menu and input/output
- `database.py` — schema, CRUD, joins, filters, sorting, and analytics
- `student.py` — Student model (`course_id`, not course name)
- `course.py` — Course model and validation
- `student_management.db` — generated automatically
- `README.md` — instructions

## Run on Mac / VS Code
1. Extract ZIP and open the `SQL-PY-006` folder in VS Code.
2. In macOS Terminal, `cd` into the folder.
3. Run: `python3 main.py`

SQLite foreign-key enforcement is enabled using `PRAGMA foreign_keys = ON` for this connection.

## Try the assignment sample
Add courses:
1 BCA, 2 BBA, 3 MCA, 4 MBA.
Then add students using course IDs:
Rahul (20, course 1, 82), Priya (21, course 1, 88), Amit (20, course 2, 76), Neha (22, course 1, 91), Rohit (21, course 2, 69).

Test course ID 99 when adding a student: expected `Invalid course ID.`.
View all students to see course names via INNER JOIN.
Courses without students should show MCA and MBA.
Course statistics use LEFT JOIN, COUNT, AVG, MAX, MIN, and GROUP BY.

## Important design notes
- `courses.course_id` is the primary key.
- `students.course_id` is a foreign key to `courses.course_id`.
- One course can have many students (one-to-many).
- A course used by students cannot be deleted because the foreign-key constraint protects referential integrity.
- A LEFT JOIN preserves courses with no students; their aggregate values can be NULL.

## GitHub commands (system Terminal)
Put the folder in your existing repository:
`python-oops-practice/SQL-Tasks/SQL-PY-006/`

From repository root:
```bash
git status
git pull --rebase
git add SQL-Tasks/SQL-PY-006/
git commit -m "Complete SQL-PY-006 relationships and joins"
git push
```
Adjust the add path if your repo layout differs.
