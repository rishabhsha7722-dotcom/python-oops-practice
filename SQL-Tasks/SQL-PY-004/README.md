# SQL-PY-004 — Student Filtering & Sorting

This project continues the Student Management System from SQL-PY-003. It keeps Add, View, Search by ID, Update, and Delete, and adds course filtering, minimum-marks filtering, partial-name search, marks sorting, and Top N students.

## Files
- `main.py` — menu, input validation, and display
- `database.py` — SQLite connection and parameterized SQL methods
- `students.db` — created automatically the first time the program runs

## Run in VS Code (Mac)
1. Extract this ZIP.
2. In VS Code, choose **File → Open Folder** and open the extracted `SQL-PY-004` folder.
3. Open `main.py`.
4. Open the macOS Terminal, change into this folder using `cd` (or use VS Code's Run Python File action), then run:
   ```bash
   python3 main.py
   ```

## Try the required tests
Add a few students first (for example, courses BCA/BBA and different marks), then test:
- Course `BCA`
- Minimum marks `80`
- Name search `ri`
- Sort marks descending and ascending
- Top N `3`
- Minimum marks `150` → `Invalid marks. Minimum marks must be between 0 and 100.`
- Top N `-5` → `Number of students must be greater than 0.`

## SQL concepts
- `WHERE` filters rows.
- `AND` requires both conditions; `OR` requires at least one.
- `LIKE` supports partial matching; `%ri%` matches names containing `ri`.
- `ORDER BY marks DESC` sorts highest to lowest; `ASC` sorts lowest to highest.
- `LIMIT ?` restricts the number of returned rows.
- User values are passed as SQL parameters (`?`) to avoid unsafe SQL string concatenation.

## GitHub
Place this folder inside your existing repository, for example:
`python-oops-practice/SQL-Tasks/SQL-PY-004/`

From macOS Terminal, go to the repository root and run:
```bash
git status
git pull --rebase
git add SQL-Tasks/SQL-PY-004/
git commit -m "Complete SQL-PY-004 filtering and sorting"
git push
```

If your repository uses a different folder path, adjust the `git add` path to match it.
