from database import Database
from student import Student


def display_students(rows):
    if not rows:
        print("No students found.")
        return

    print("\nID | Name | Age | Course | Marks")
    print("-" * 45)
    for row in rows:
        student_id, name, age, course, marks = row
        print(f"{student_id} | {name} | {age} | {course} | {marks}")


def add_student(database):
    try:
        student_id = int(input("Student ID: "))
        name = input("Name: ")
        age = int(input("Age: "))
        course = input("Course: ")
        marks = float(input("Marks (0-100): "))

        student = Student(student_id, name, age, course, marks)
        database.add_student(student)
        print("Student stored successfully.")
    except ValueError as error:
        print(f"Invalid input: {error}")
    except RuntimeError as error:
        print(error)


def search_student(database):
    try:
        student_id = int(input("Enter student ID to search: "))
        row = database.get_student_by_id(student_id)
        if row:
            display_students([row])
        else:
            print("Student not found.")
    except ValueError:
        print("Student ID must be an integer.")
    except RuntimeError as error:
        print(error)


def main():
    database = Database()

    try:
        database.connect()
        database.create_table()
        print("Connected to SQLite. Students table is ready.")

        while True:
            print("\n===== Student Management System =====")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student by ID")
            print("4. Exit")

            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                add_student(database)
            elif choice == "2":
                try:
                    display_students(database.get_all_students())
                except RuntimeError as error:
                    print(error)
            elif choice == "3":
                search_student(database)
            elif choice == "4":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")

    except RuntimeError as error:
        print(error)
    finally:
        database.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
