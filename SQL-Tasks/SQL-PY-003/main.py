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

def add_student(db):
    try:
        student = Student(int(input("Student ID: ")), input("Name: "),
                         int(input("Age: ")), input("Course: "),
                         float(input("Marks (0-100): ")))
        db.add_student(student)
        print("Student added successfully.")
    except ValueError as error:
        print(f"Input/database validation: {error}")
    except RuntimeError as error:
        print(error)

def search_student(db, ask_id=True):
    try:
        sid = int(input("Student ID: ")) if ask_id else None
        row = db.get_student_by_id(sid)
        if row:
            display_students([row])
        else:
            print("Student not found.")
        return row
    except ValueError:
        print("Student ID must be an integer.")
    except RuntimeError as error:
        print(error)
    return None

def update_student(db):
    try:
        sid = int(input("Student ID to update: "))
        existing = db.get_student_by_id(sid)
        if existing is None:
            print("Student not found.")
            return

        print("Current record:")
        display_students([existing])
        print("Enter the new details (student ID remains unchanged).")
        updated = Student(
            sid,
            input("New name: "),
            int(input("New age: ")),
            input("New course: "),
            float(input("New marks (0-100): "))
        )
        count = db.update_student(updated)
        if count == 0:
            print("No matching student was updated.")
        else:
            print("Student updated successfully.")
    except ValueError as error:
        print(f"Update validation error: {error}")
    except RuntimeError as error:
        print(error)

def delete_student(db):
    try:
        sid = int(input("Student ID to delete: "))
        existing = db.get_student_by_id(sid)
        if existing is None:
            print("Student not found.")
            return

        print("Student selected for deletion:")
        display_students([existing])
        confirm = input("Delete this student? Type yes to confirm: ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return

        count = db.delete_student(sid)
        if count == 0:
            print("Student not found.")
        else:
            print("Student deleted successfully.")
    except ValueError:
        print("Student ID must be an integer.")
    except RuntimeError as error:
        print(error)

def main():
    db = Database()
    try:
        db.connect()
        db.create_table()
        print("Student database ready.")
        while True:
            print("\n===== Student Management System =====")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")
            choice = input("Choose an option (1-6): ").strip()

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
                update_student(db)
            elif choice == "5":
                delete_student(db)
            elif choice == "6":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please select 1-6.")
    except RuntimeError as error:
        print(error)
    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
