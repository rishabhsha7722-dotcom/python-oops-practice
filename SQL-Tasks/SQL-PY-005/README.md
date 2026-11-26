# SQL-PY-005 — Student Performance Analytics

This continues SQL-PY-004. Existing CRUD, course/name/marks filtering, sorting, and Top N features remain. The new task adds database-side aggregate analytics and course grouping.

## Project files
- `main.py` — 13-option menu and input/output
- `database.py` — SQLite queries, CRUD, filters, and analytics methods
- `students.db` — generated automatically on first run

## Run (Mac + VS Code)
1. Download and extract the ZIP.
2. Open the extracted `SQL-PY-005` folder in VS Code.
3. Open macOS Terminal and `cd` to the folder.
4. Run `python3 main.py`.

## New analytics methods
`get_total_students()`, `get_average_marks()`, `get_total_marks()`, `get_highest_marks()`, `get_lowest_marks()`, `get_course_statistics()`, `get_course_average_marks()`, `get_course_highest_marks()`, `get_course_lowest_marks()`, `get_courses_above_average(min_average)`.

The aggregate values are calculated in SQL—not by loading all records into Python and looping. Empty-table `AVG`, `SUM`, `MIN`, and `MAX` return SQL `NULL`; this app safely displays them as 0 for readable empty-database statistics.

## Test
Add at least 3 BCA students and 2 BBA students. Verify:
- COUNT equals the actual number of students.
- AVG equals a manual calculation.
- MAX/MIN are correct.
- Course statistics show course counts and averages.
- HAVING threshold 80 returns only courses with average >= 80.
- Start with no records: analytics menu should not crash.

## GitHub (system Terminal)
Place the folder under your existing repository, e.g.:
`python-oops-practice/SQL-Tasks/SQL-PY-005/`

From the repository root:
```bash
git status
git pull --rebase
git add SQL-Tasks/SQL-PY-005/
git commit -m "Complete SQL-PY-005 student performance analytics"
git push
```
Adjust the `git add` path if your task folders are arranged differently.
