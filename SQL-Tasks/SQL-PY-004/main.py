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
            print("Marks must be a number.")
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

        return {
            "student_id": student_id,
            "name": name,
            "age": age,
            "course": course,
            "marks": marks,
        }


def print_students(rows):
    if not rows:
        print("No students found.")
        return
    print("-" * 72)
    print(f"{'ID':<8}{'Name':<22}{'Age':<8}{'Course':<16}{'Marks':<10}")
    print("-" * 72)
    for student_id, name, age, course, marks in rows:
        print(f"{student_id:<8}{name:<22}{age:<8}{course:<16}{marks:<10.2f}")
    print("-" * 72)


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
11. Exit
""")
            choice = input("Choose an option (1-11): ").strip()

            try:
                if choice == "1":
                    student = read_student()
                    db.add_student(student)
                    print("Student added successfully.")

                elif choice == "2":
                    print_students(db.get_all_students())

                elif choice == "3":
                    student_id = read_int("Enter student ID: ")
                    row = db.get_student_by_id(student_id)
                    print_students([row] if row else [])

                elif choice == "4":
                    course = input("Enter course: ").strip()
                    if not course:
                        print("Course cannot be empty.")
                    else:
                        print_students(db.get_students_by_course(course))

                elif choice == "5":
                    keyword = input("Enter all or part of the name: ").strip()
                    if not keyword:
                        print("Search keyword cannot be empty.")
                    else:
                        print_students(db.search_students_by_name(keyword))

                elif choice == "6":
                    min_marks = float(input("Enter minimum marks (0-100): ").strip())
                    if not 0 <= min_marks <= 100:
                        print("Invalid marks. Minimum marks must be between 0 and 100.")
                    else:
                        print_students(db.get_students_by_marks(min_marks))

                elif choice == "7":
                    direction = input("Sort order: A for ascending, D for descending [D]: ").strip().upper()
                    if direction not in ("", "A", "D"):
                        print("Enter A or D.")
                    else:
                        print_students(db.get_students_sorted_by_marks(desc=(direction != "A")))

                elif choice == "8":
                    limit = read_int("How many top students? ")
                    if limit <= 0:
                        print("Number of students must be greater than 0.")
                    else:
                        print_students(db.get_top_students(limit))

                elif choice == "9":
                    student_id = read_int("Enter student ID to update: ")
                    if not db.get_student_by_id(student_id):
                        print("Student ID not found.")
                    else:
                        student = read_student(existing_id=student_id)
                        changed = db.update_student(student_id, student)
                        print("Student updated successfully." if changed else "No changes made.")

                elif choice == "10":
                    student_id = read_int("Enter student ID to delete: ")
                    if not db.get_student_by_id(student_id):
                        print("Student ID not found.")
                    elif input("Delete this student? (y/n): ").strip().lower() == "y":
                        print("Student deleted successfully." if db.delete_student(student_id) else "Delete failed.")
                    else:
                        print("Delete cancelled.")

                elif choice == "11":
                    print("Goodbye!")
                    break

                else:
                    print("Invalid option. Choose from 1 to 11.")

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as error:
                print(f"Operation failed: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
