from database import Database
from student import Student

def display_students(rows):
    if not rows:
        print("No students found.")
        return
    print("\nID | Name | Age | Course | Marks")
    print("-" * 48)
    for sid, name, age, course, marks in rows:
        print(f"{sid} | {name} | {age} | {course} | {marks}")

def add_student(database):
    try:
        student = Student(int(input("Student ID: ")), input("Name: "),
                         int(input("Age: ")), input("Course: "),
                         float(input("Marks (0-100): ")))
        database.add_student(student)
        print("Student added successfully.")
    except ValueError as error:
        print(f"Input/database validation: {error}")
    except RuntimeError as error:
        print(error)

def search_student(database):
    try:
        sid = int(input("Enter student ID to search: "))
        row = database.get_student_by_id(sid)
        display_students([row] if row else [])
        if row is None:
            print("Student not found.")
    except ValueError:
        print("Student ID must be an integer.")
    except RuntimeError as error:
        print(error)

def main():
    db = Database()
    try:
        db.connect()
        db.create_table()
        print("Connected. Constrained students table is ready.")
        while True:
            print("\n===== Student Management System =====")
            print("1. Add Student\n2. View All Students\n3. Search Student by ID\n4. Exit")
            choice = input("Choose an option (1-4): ").strip()
            if choice == "1":
                add_student(db)
            elif choice == "2":
                try:
                    display_students(db.get_all_students())
                except RuntimeError as error:
                    print(error)
            elif choice == "3":
                search_student(db)
            elif choice == "4":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Enter 1, 2, 3, or 4.")
    except RuntimeError as error:
        print(error)
    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
