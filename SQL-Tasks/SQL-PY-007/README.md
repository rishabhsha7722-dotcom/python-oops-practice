# SQL-PY-007 — Database Transactions & ACID

Part of the progressive **Student Management System** (SQL-PY-001 → SQL-PY-010).
This task adds **transactions** so multi-step database changes are *all-or-nothing*.

## What's new
- `student_course_history` table (audit log of every course change)
- `transfer_student_course()` — UPDATE + INSERT inside **one** transaction
- `begin_transaction()`, `commit()`, `rollback()`
- `get_course_history()`, `get_student_course_history()`, `create_history_table()`
- Menu options **15** (Transfer) and **16** (View Transfer History)

## Project structure
```
SQL-PY-007/
├── main.py                  # menu (17 options)
├── database.py              # all SQL + transaction logic
├── student.py               # Student model + validation
├── course.py                # Course model + validation
├── student_management.db    # created automatically on first run
└── README.md
```

## How to run
```bash
python main.py     # creates student_management.db + sample data on first run
```
Requires Python 3.8+ — no external packages (only the built-in `sqlite3`).

## How the transfer works
```
validate (student? course? same course?)   <- no DB change possible here
        ↓
BEGIN
        ↓
UPDATE students SET course_id = ?
        ↓
INSERT INTO student_course_history ...
        ↓
COMMIT            (if any step raised an error → ROLLBACK)
```
Validation runs **before** `BEGIN`, so invalid input never opens a transaction.
Menu option 15 lets you answer `y` to *"Simulate a failure"* to watch ROLLBACK live.

## Tests (run manually from the menu)
| # | Scenario | Expected |
|---|----------|----------|
| 1 | Rahul BCA → MCA | Student updated, history added, committed |
| 2 | Student ID 999 | Rejected, no change |
| 3 | Course ID 99 | Rejected, no change |
| 4 | BCA → BCA | "already enrolled" message |
| 5 | Option 15, answer `y` to "Simulate a failure" | Rolled back: Rahul stays in BCA, no history row |

## ACID
| Property | Meaning | In this project |
|---|---|---|
| Atomicity | All or nothing | Test 5: failed transfer leaves Rahul in BCA |
| Consistency | DB valid before & after | FK constraints + validation + CHECKs |
| Isolation | Transactions don't interfere | SQLite locks the DB during a write transaction |
| Durability | Committed data survives | Close the program, reopen: the transfer is still there |

## SQL queries
```sql
-- Update a student's course
UPDATE students SET course_id = ? WHERE student_id = ?;

-- Insert course history
INSERT INTO student_course_history (student_id, old_course_id, new_course_id)
VALUES (?, ?, ?);

-- Complete transfer history
SELECT * FROM student_course_history;

-- Readable history with JOINs
SELECT s.name AS student_name, oc.course_name AS old_course,
       nc.course_name AS new_course, h.changed_at AS transfer_date
FROM student_course_history h
JOIN students s  ON s.student_id = h.student_id
JOIN courses  oc ON oc.course_id = h.old_course_id
JOIN courses  nc ON nc.course_id = h.new_course_id
ORDER BY h.changed_at;
```

## Assignment answers
### Basic
1. **Transaction** – a group of database operations treated as one unit of work.
2. **COMMIT** – permanently saves all changes made in the transaction.
3. **ROLLBACK** – cancels all uncommitted changes of the current transaction.
4. **Why needed** – to prevent partial updates when one of several related operations fails.
5. **Atomicity example** – changing Rahul's course needs UPDATE + INSERT history. If the INSERT fails, the UPDATE is undone, so Rahul stays in his old course.

### Intermediate
1. **ACID** – *Atomicity* (all or nothing), *Consistency* (valid state before and after), *Isolation* (concurrent transactions don't improperly interfere), *Durability* (committed data survives crashes/restarts).
2. **Exception before commit()** – nothing is saved; we call `rollback()` and the database returns to its state before `BEGIN`.
3. **Partial update** – only some of the required operations were saved (e.g. course changed but no history row) leaving inconsistent data.
4. **Validate before the transaction** – invalid input is rejected cheaply without opening a transaction or holding database locks, and rollback is reserved for unexpected failures.
5. **commit() vs rollback()** – commit makes changes permanent; rollback discards them.

## Viva quick answers
- *Problem solved by transactions?* Prevents partial updates by treating related operations as a single unit.
- *COMMIT?* Changes become permanent.
- *ROLLBACK?* Cancels uncommitted changes.
- *Real-world example?* Bank transfer (debit A + credit B).
- *ACID?* Atomicity, Consistency, Isolation, Durability.
- *"All or nothing"?* Atomicity.
