"""main.py - Menu for the Student Management System (SQL-PY-007)."""
from database import Database
from student import Student
from course import Course

MENU = """
========== STUDENT MANAGEMENT SYSTEM ==========
 1. Add Course                 10. Update Student
 2. View Courses               11. Delete Student
 3. Add Student                12. Student Statistics
 4. View All Students          13. Course-wise Statistics
 5. Search Student             14. Courses Without Students
 6. Search Students by Course  15. Transfer Student Course
 7. Search Students by Marks   16. View Course Transfer History
 8. Sort Students              17. Exit
 9. Top N Students
==============================================="""


def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("  Please enter a whole number.")
        return None


def read_float(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("  Please enter a number.")
        return None


def show_students(rows):
    if not rows:
        print("  No students found.")
        return
    print(f"  {'ID':<4}{'Name':<12}{'Age':<5}{'Email':<24}{'Marks':<8}Course")
    for r in rows:
        print(f"  {r['student_id']:<4}{r['name']:<12}{r['age']:<5}{r['email']:<24}"
              f"{r['marks']:<8}{r['course_name']}")


def show_courses(rows):
    if not rows:
        print("  No courses found.")
        return
    for r in rows:
        print(f"  [{r['course_id']}] {r['course_name']} ({r['duration_years']} yrs)")


def show_history(rows):
    if not rows:
        print("  No course transfers recorded yet.")
        return
    print(f"  {'#':<4}{'Student':<12}{'Old':<8}{'New':<8}Date")
    for r in rows:
        print(f"  {r['history_id']:<4}{r['student_name']:<12}{r['old_course']:<8}"
              f"{r['new_course']:<8}{r['changed_at']}")


def main():
    db = Database()
    if db.seed_sample_data():
        print("Sample data loaded (first run).")

    while True:
        print(MENU)
        choice = input("Enter choice (1-17): ").strip()

        if choice == "1":
            name = input("Course name: ")
            years = read_int("Duration (years): ")
            if years is not None:
                print(" ", db.add_course(Course(name, years))[1])

        elif choice == "2":
            show_courses(db.get_all_courses())

        elif choice == "3":
            name = input("Name: ")
            age = read_int("Age: ")
            email = input("Email: ")
            marks = read_float("Marks (0-100): ")
            show_courses(db.get_all_courses())
            course_id = read_int("Course ID: ")
            if None not in (age, marks, course_id):
                print(" ", db.add_student(Student(name, age, email, marks, course_id))[1])

        elif choice == "4":
            show_students(db.get_all_students())

        elif choice == "5":
            show_students(db.search_student_by_name(input("Name to search: ")))

        elif choice == "6":
            show_students(db.search_students_by_course(input("Course name: ")))

        elif choice == "7":
            low = read_float("Minimum marks: ")
            high = read_float("Maximum marks: ")
            if None not in (low, high):
                show_students(db.search_students_by_marks(low, high))

        elif choice == "8":
            col = input("Sort by (name/age/marks/student_id): ").strip().lower()
            desc = input("Descending? (y/n): ").strip().lower() == "y"
            show_students(db.sort_students(col, desc))

        elif choice == "9":
            n = read_int("How many top students? ")
            if n is not None:
                show_students(db.get_top_students(n))

        elif choice == "10":
            sid = read_int("Student ID: ")
            if sid is not None and db.get_student_by_id(sid):
                name = input("New name: ")
                age = read_int("New age: ")
                email = input("New email: ")
                marks = read_float("New marks: ")
                if None not in (age, marks):
                    print(" ", db.update_student(sid, name, age, email.strip().lower(), marks)[1])
            elif sid is not None:
                print("  Student not found.")

        elif choice == "11":
            sid = read_int("Student ID to delete: ")
            if sid is not None:
                print(" ", db.delete_student(sid)[1])

        elif choice == "12":
            s = db.get_student_statistics()
            print(f"  Total: {s['total']} | Average: {s['average']} | "
                  f"Highest: {s['highest']} | Lowest: {s['lowest']}")

        elif choice == "13":
            for r in db.get_course_statistics():
                print(f"  {r['course_name']:<6} students: {r['total_students']:<3} "
                      f"avg marks: {r['average_marks']}")

        elif choice == "14":
            rows = db.get_courses_without_students()
            if rows:
                for r in rows:
                    print(f"  [{r['course_id']}] {r['course_name']}")
            else:
                print("  Every course has at least one student.")

        elif choice == "15":
            show_students(db.get_all_students())
            show_courses(db.get_all_courses())
            sid = read_int("Student ID: ")
            cid = read_int("New Course ID: ")
            if None not in (sid, cid):
                fail = input("Simulate a failure to demo ROLLBACK? (y/n): ").strip().lower() == "y"
                ok, msg = db.transfer_student_course(sid, cid, simulate_failure=fail)
                print(("  OK: " if ok else "  FAILED: ") + msg)

        elif choice == "16":
            print("  1. All history   2. One student")
            if input("  Choose: ").strip() == "2":
                sid = read_int("Student ID: ")
                if sid is not None:
                    show_history(db.get_student_course_history(sid))
            else:
                show_history(db.get_course_history())

        elif choice == "17":
            db.close()
            print("Goodbye!")
            break

        else:
            print("  Invalid choice. Enter a number from 1 to 17.")


if __name__ == "__main__":
    main()
