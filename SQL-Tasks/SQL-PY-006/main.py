from database import Database
from course import Course
from student import Student


def integer(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")


def make_student(existing_id=None):
    sid = existing_id if existing_id is not None else integer("Student ID: ")
    name = input("Name: ").strip()
    age = integer("Age: ")
    course_id = integer("Course ID: ")
    try:
        marks = float(input("Marks (0-100): ").strip())
    except ValueError:
        raise ValueError("Marks must be numeric.")
    student = Student(sid, name, age, course_id, marks)
    student.validate()
    return student


def show_courses(rows):
    if not rows:
        print("No courses found.")
    for cid, name in rows:
        print(f"Course ID: {cid} | Course: {name}")


def show_students(rows):
    if not rows:
        print("No students found.")
        return
    print(f"{'ID':<7}{'Name':<20}{'Course':<14}{'Marks':<8}")
    print("-" * 52)
    for row in rows:
        # Rows from joined student listing/search: id,name,course_name,marks
        print(f"{row[0]:<7}{row[1]:<20}{row[2]:<14}{row[3]:<8.2f}")


def show_stats(rows):
    if not rows:
        print("No course statistics.")
        return
    print(f"{'Course':<12}{'Count':<8}{'Average':<12}{'Highest':<10}{'Lowest':<10}")
    for course, count, avg, high, low in rows:
        print(f"{course:<12}{count:<8}{(avg or 0):<12.2f}{(high or 0):<10.2f}{(low or 0):<10.2f}")


def main():
    db = Database()
    try:
        while True:
            print("""
====== Student Management System ======
1. Add Course
2. View Courses
3. Add Student
4. View All Students
5. Search Student
6. Search Students by Course
7. Search Students by Marks
8. Sort Students
9. Top N Students
10. Update Student
11. Delete Student
12. Student Statistics
13. Course-wise Statistics
14. Courses Without Students
15. Exit
""")
            choice = input("Select (1-15): ").strip()
            try:
                if choice == "1":
                    cid = integer("Course ID: ")
                    cname = input("Course name: ").strip()
                    db.add_course(Course(cid, cname))
                    print("Course added.")
                elif choice == "2":
                    show_courses(db.get_all_courses())
                elif choice == "3":
                    db.add_student(make_student())
                    print("Student added.")
                elif choice == "4":
                    show_students(db.get_all_students())
                elif choice == "5":
                    sid = integer("Student ID: ")
                    row = db.get_student_by_id(sid)
                    if row:
                        show_students([(row[0], row[1], row[4], row[5])])
                    else:
                        print("Student not found.")
                elif choice == "6":
                    course = input("Course name (e.g. BCA): ").strip()
                    if not course:
                        print("Course cannot be empty.")
                    else:
                        show_students(db.get_students_by_course(course))
                elif choice == "7":
                    min_marks = float(input("Minimum marks 0-100: "))
                    if not 0 <= min_marks <= 100:
                        print("Minimum marks must be between 0 and 100.")
                    else:
                        show_students(db.get_students_by_marks(min_marks))
                elif choice == "8":
                    d = input("A ascending / D descending [D]: ").strip().upper()
                    if d not in ("", "A", "D"):
                        print("Enter A or D.")
                    else:
                        show_students(db.get_students_sorted_by_marks(d != "A"))
                elif choice == "9":
                    n = integer("Top N: ")
                    if n <= 0:
                        print("Number of students must be greater than 0.")
                    else:
                        show_students(db.get_top_students(n))
                elif choice == "10":
                    sid = integer("Student ID to update: ")
                    if not db.get_student_by_id(sid):
                        print("Student not found.")
                    else:
                        db.update_student(sid, make_student(existing_id=sid))
                        print("Student updated.")
                elif choice == "11":
                    sid = integer("Student ID to delete: ")
                    if input("Confirm delete? (y/n): ").strip().lower() == "y":
                        print("Deleted." if db.delete_student(sid) else "Student not found.")
                elif choice == "12":
                    print(f"Total students: {db.get_total_students()}")
                    print(f"Total marks: {db.get_total_marks():.2f}")
                    print(f"Average marks: {db.get_average_marks():.2f}")
                    print(f"Highest marks: {db.get_highest_marks():.2f}")
                    print(f"Lowest marks: {db.get_lowest_marks():.2f}")
                elif choice == "13":
                    show_stats(db.get_course_statistics())
                elif choice == "14":
                    courses = db.get_courses_without_students()
                    if courses:
                        print("Courses without students:")
                        for (name,) in courses:
                            print(name)
                    else:
                        print("Every course currently has at least one student (or no courses exist).")
                elif choice == "15":
                    print("Goodbye!")
                    break
                else:
                    print("Choose a menu number from 1 to 15.")
            except sqlite3.IntegrityError as e:
                print(f"Database constraint error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"Operation failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sqlite3
    main()
