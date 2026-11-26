from database import Database


def read_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid whole number.")


def read_student(existing_id=None):
    while True:
        student_id = existing_id if existing_id is not None else read_int("Student ID: ")
        name = input("Name: ").strip()
        age = read_int("Age: ")
        course = input("Course: ").strip()
        try:
            marks = float(input("Marks (0-100): ").strip())
        except ValueError:
            print("Marks must be numeric.")
            continue
        if not name:
            print("Name cannot be empty.")
            continue
        if age <= 0:
            print("Age must be greater than 0.")
            continue
        if not course:
            print("Course cannot be empty.")
            continue
        if not 0 <= marks <= 100:
            print("Invalid marks. Marks must be between 0 and 100.")
            continue
        return {"student_id": student_id, "name": name, "age": age,
                "course": course, "marks": marks}


def print_students(rows):
    if not rows:
        print("No students found.")
        return
    print("-" * 72)
    print(f"{'ID':<8}{'Name':<22}{'Age':<8}{'Course':<16}{'Marks':<10}")
    print("-" * 72)
    for sid, name, age, course, marks in rows:
        print(f"{sid:<8}{name:<22}{age:<8}{course:<16}{marks:<10.2f}")
    print("-" * 72)


def print_course_stats(rows):
    if not rows:
        print("No course data available.")
        return
    print(f"{'Course':<14}{'Students':<12}{'Average':<12}{'Highest':<12}{'Lowest':<12}")
    print("-" * 62)
    for course, count, avg, high, low in rows:
        print(f"{course:<14}{count:<12}{avg:<12.2f}{high:<12.2f}{low:<12.2f}")


def main():
    db = Database()
    try:
        while True:
            print("""
====== Student Management System ======
1. Add Student
2. View All Students
3. Search Student by ID
4. Search Student by Course
5. Search Student by Name
6. Filter Students by Marks
7. Sort Students by Marks
8. Top N Students
9. Update Student
10. Delete Student
11. Student Statistics
12. Course-wise Statistics
13. Exit
""")
            choice = input("Choose an option (1-13): ").strip()
            try:
                if choice == "1":
                    db.add_student(read_student())
                    print("Student added successfully.")
                elif choice == "2":
                    print_students(db.get_all_students())
                elif choice == "3":
                    row = db.get_student_by_id(read_int("Student ID: "))
                    print_students([row] if row else [])
                elif choice == "4":
                    course = input("Course: ").strip()
                    if not course:
                        print("Course cannot be empty.")
                    else:
                        print_students(db.get_students_by_course(course))
                elif choice == "5":
                    keyword = input("Name or part of name: ").strip()
                    if not keyword:
                        print("Search keyword cannot be empty.")
                    else:
                        print_students(db.search_students_by_name(keyword))
                elif choice == "6":
                    min_marks = float(input("Minimum marks (0-100): ").strip())
                    if not 0 <= min_marks <= 100:
                        print("Invalid marks. Minimum marks must be between 0 and 100.")
                    else:
                        print_students(db.get_students_by_marks(min_marks))
                elif choice == "7":
                    direction = input("A=ascending, D=descending [D]: ").strip().upper()
                    if direction not in ("", "A", "D"):
                        print("Please enter A or D.")
                    else:
                        print_students(db.get_students_sorted_by_marks(desc=(direction != "A")))
                elif choice == "8":
                    limit = read_int("Top how many students? ")
                    if limit <= 0:
                        print("Number of students must be greater than 0.")
                    else:
                        print_students(db.get_top_students(limit))
                elif choice == "9":
                    sid = read_int("Student ID to update: ")
                    if db.get_student_by_id(sid) is None:
                        print("Student ID not found.")
                    else:
                        updated = db.update_student(sid, read_student(existing_id=sid))
                        print("Student updated." if updated else "No changes made.")
                elif choice == "10":
                    sid = read_int("Student ID to delete: ")
                    if db.get_student_by_id(sid) is None:
                        print("Student ID not found.")
                    elif input("Confirm delete (y/n): ").strip().lower() == "y":
                        print("Student deleted." if db.delete_student(sid) else "Delete failed.")
                    else:
                        print("Delete cancelled.")
                elif choice == "11":
                    print("\n--- Student Statistics ---")
                    print(f"Total Students : {db.get_total_students()}")
                    print(f"Total Marks    : {db.get_total_marks():.2f}")
                    print(f"Average Marks  : {db.get_average_marks():.2f}")
                    print(f"Highest Marks  : {db.get_highest_marks():.2f}")
                    print(f"Lowest Marks   : {db.get_lowest_marks():.2f}")
                    if db.get_total_students() == 0:
                        print("(Database is empty; statistics show 0.)")
                elif choice == "12":
                    print("\n--- Course-wise Statistics ---")
                    print_course_stats(db.get_course_statistics())
                    if db.get_total_students() > 0:
                        try:
                            threshold = float(input("Minimum course average for HAVING filter (0-100, or Enter to skip): ").strip() or "-1")
                            if threshold >= 0:
                                if threshold > 100:
                                    print("Minimum average must be between 0 and 100.")
                                else:
                                    print("\nCourses with average marks >= threshold:")
                                    qualifying = db.get_courses_above_average(threshold)
                                    if not qualifying:
                                        print("No courses meet this average.")
                                    else:
                                        for course, avg in qualifying:
                                            print(f"{course}: {avg:.2f}")
                        except ValueError:
                            print("Invalid threshold; skipped HAVING filter.")
                elif choice == "13":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Select 1-13.")
            except ValueError:
                print("Please enter a valid numeric value.")
            except Exception as exc:
                print(f"Operation failed: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
