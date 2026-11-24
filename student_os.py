import json
import math
from pathlib import Path

# Persistence: keep the data file beside this script.
DATA_FILE = Path(__file__).with_name("students_data.json")


def load_records():
    """Load valid student records; safely return an empty dictionary on bad files."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load student records: {error}")
        return {}

    if not isinstance(data, dict):
        print("Could not load student records: the data file must contain a JSON object.")
        return {}

    records = {}
    for student_id, student in data.items():
        if not isinstance(student_id, str) or not student_id.strip() or not isinstance(student, dict):
            continue
        name = student.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        try:
            grade = float(student.get("grade"))
        except (TypeError, ValueError):
            continue
        if math.isfinite(grade) and 0.0 <= grade <= 10.0:
            records[student_id] = {"name": name.strip(), "grade": grade}
    return records


def save_records(students):
    """Save records as readable JSON, reporting success or failure."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False, allow_nan=False)
            file.write("\n")
    except (OSError, TypeError, ValueError) as error:
        print(f"Could not save student records: {error}")
        return False
    print("Records saved successfully.")
    return True


def read_nonblank(prompt, field_name):
    """Prompt repeatedly until a non-empty, trimmed string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be blank.")


def read_grade():
    """Read a finite numeric grade in the inclusive range 0.0–10.0."""
    while True:
        raw_grade = input("Grade (0.0 to 10.0): ").strip()
        if not raw_grade:
            print("Grade cannot be blank.")
            continue
        try:
            grade = float(raw_grade)
        except ValueError:
            print("Please enter a numeric grade.")
            continue
        if not math.isfinite(grade) or not 0.0 <= grade <= 10.0:
            print("Grade must be between 0.0 and 10.0.")
            continue
        return grade


def add_student(students):
    """Prompt for a new record and reject duplicate IDs."""
    student_id = read_nonblank("Student ID: ", "Student ID")
    if student_id in students:
        print("This ID already exists.")
        return
    name = read_nonblank("Name: ", "Name")
    grade = read_grade()
    students[student_id] = {"name": name, "grade": grade}
    print("Student added successfully.")


def view_students(students):
    """Display records in an aligned table or report an empty collection."""
    if not students:
        print("No student records found.")
        return

    id_width = max(len("ID"), *(len(student_id) for student_id in students))
    name_width = max(len("Name"), *(len(student["name"]) for student in students.values()))
    grade_width = len("Grade")
    border = f"+{'-' * (id_width + 2)}+{'-' * (name_width + 2)}+{'-' * (grade_width + 2)}+"
    print(border)
    print(f"| {'ID':<{id_width}} | {'Name':<{name_width}} | {'Grade':>{grade_width}} |")
    print(border)
    for student_id, student in sorted(students.items()):
        print(f"| {student_id:<{id_width}} | {student['name']:<{name_width}} | {student['grade']:>{grade_width}.1f} |")
    print(border)


def search_student(students):
    """Find and display one student by ID."""
    student_id = read_nonblank("Student ID to search: ", "Student ID")
    student = students.get(student_id)
    if student is None:
        print("Student record not found.")
        return
    print(f"ID: {student_id}\nName: {student['name']}\nGrade: {student['grade']:.1f}")


def update_student(students):
    """Update either or both fields; blank update responses keep current values."""
    student_id = read_nonblank("Student ID to update: ", "Student ID")
    student = students.get(student_id)
    if student is None:
        print("Student record not found.")
        return

    print("Press Enter to keep a value unchanged.")
    name = input(f"Name [{student['name']}]: ").strip()
    if name:
        student["name"] = name

    while True:
        raw_grade = input(f"Grade (0.0 to 10.0) [{student['grade']:.1f}]: ").strip()
        if not raw_grade:
            break
        try:
            grade = float(raw_grade)
        except ValueError:
            print("Please enter a numeric grade or press Enter to keep the current grade.")
            continue
        if not math.isfinite(grade) or not 0.0 <= grade <= 10.0:
            print("Grade must be between 0.0 and 10.0.")
            continue
        student["grade"] = grade
        break
    print("Student updated successfully.")


def main():
    """Load records, run the required menu loop, and save on Save or Exit."""
    students = load_records()
    while True:
        print("\nSTUDENT OS MAIN MENU")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Update Student Details")
        print("5. Save Records")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            save_records(students)
        elif choice == "6":
            save_records(students)
            print("Goodbye.")
            break
        else:
            print("Please enter a valid choice.")


if __name__ == "__main__":
    main()
