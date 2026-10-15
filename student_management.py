"""
Student Management System
=========================
Features:
- Add, Update, Delete, Search student records
- Store data using JSON files
- Sort records by name or marks
- Admin login authentication
- Generate reports (topper, average marks, etc.)
- Exception handling for invalid inputs
- Modular and well-commented code

Author: MCA III Semester Student
"""

import json
import os
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================
DATA_FILE = "students.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# DATA HANDLING
# ============================================================

def load_students():
    """Load student records from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []


def save_students(students):
    """Save student records to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save data: {e}")
        return False


def generate_id(students):
    """Generate next student ID (S001, S002, ...)."""
    if not students:
        return "S001"
    max_num = 0
    for s in students:
        try:
            num = int(s["id"][1:])
            if num > max_num:
                max_num = num
        except:
            pass
    return f"S{max_num + 1:03d}"


# ============================================================
# AUTHENTICATION
# ============================================================

def admin_login():
    """Admin login with username and password."""
    print("\n" + "=" * 45)
    print("           ADMIN LOGIN")
    print("=" * 45)
    
    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\n✅ Login successful! Welcome Admin.")
            return True
        else:
            attempts -= 1
            print(f"❌ Invalid credentials! Attempts left: {attempts}")
    
    print("\n⛔ Too many failed attempts. Exiting...")
    return False


# ============================================================
# CORE OPERATIONS
# ============================================================

def add_student(students):
    """Add a new student record."""
    print("\n--- Add New Student ---")
    
    try:
        name = input("Name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
        
        age = int(input("Age: ").strip())
        if age < 15 or age > 50:
            print("❌ Age must be between 15 and 50!")
            return
        
        course = input("Course (MCA/BCA/B.Tech etc.): ").strip()
        if not course:
            print("❌ Course cannot be empty!")
            return
        
        marks = float(input("Marks (0-100): ").strip())
        if marks < 0 or marks > 100:
            print("❌ Marks must be between 0 and 100!")
            return
        
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        
        student = {
            "id": generate_id(students),
            "name": name,
            "age": age,
            "course": course,
            "marks": marks,
            "email": email,
            "phone": phone
        }
        
        students.append(student)
        save_students(students)
        print(f"\n✅ Student added successfully! ID: {student['id']}")
        
    except ValueError:
        print("❌ Invalid input! Please enter correct data types.")
    except Exception as e:
        print(f"❌ Error: {e}")


def display_students(students, title="All Students"):
    """Display student records in a table format."""
    if not students:
        print("\n📭 No student records found.")
        return
    
    print(f"\n{'=' * 80}")
    print(f"  {title} ({len(students)} records)")
    print(f"{'=' * 80}")
    print(f"{'ID':<8}{'Name':<20}{'Age':<6}{'Course':<12}{'Marks':<8}{'Phone':<15}")
    print("-" * 80)
    
    for s in students:
        print(f"{s['id']:<8}{s['name']:<20}{s['age']:<6}{s['course']:<12}{s['marks']:<8}{s.get('phone', '-'):<15}")
    
    print("=" * 80)


def search_student(students):
    """Search student by ID or Name."""
    print("\n--- Search Student ---")
    print("1. Search by ID")
    print("2. Search by Name")
    
    try:
        choice = int(input("Choice: ").strip())
        
        if choice == 1:
            sid = input("Enter Student ID (e.g. S001): ").strip().upper()
            results = [s for s in students if s["id"].upper() == sid]
        elif choice == 2:
            name = input("Enter Name (partial match ok): ").strip().lower()
            results = [s for s in students if name in s["name"].lower()]
        else:
            print("❌ Invalid choice!")
            return
        
        if results:
            display_students(results, "Search Results")
        else:
            print("\n❌ No matching student found.")
            
    except ValueError:
        print("❌ Please enter a valid number!")


def update_student(students):
    """Update an existing student record."""
    print("\n--- Update Student ---")
    sid = input("Enter Student ID to update: ").strip().upper()
    
    student = None
    for s in students:
        if s["id"].upper() == sid:
            student = s
            break
    
    if not student:
        print("❌ Student not found!")
        return
    
    print(f"\nCurrent details of {student['name']}:")
    print(f"  Age: {student['age']} | Course: {student['course']} | Marks: {student['marks']}")
    print("\nLeave blank to keep current value.")
    
    try:
        name = input(f"New Name [{student['name']}]: ").strip()
        if name:
            student["name"] = name
        
        age_str = input(f"New Age [{student['age']}]: ").strip()
        if age_str:
            age = int(age_str)
            if 15 <= age <= 50:
                student["age"] = age
            else:
                print("⚠ Age not updated (invalid range)")
        
        course = input(f"New Course [{student['course']}]: ").strip()
        if course:
            student["course"] = course
        
        marks_str = input(f"New Marks [{student['marks']}]: ").strip()
        if marks_str:
            marks = float(marks_str)
            if 0 <= marks <= 100:
                student["marks"] = marks
            else:
                print("⚠ Marks not updated (invalid range)")
        
        email = input(f"New Email [{student.get('email', '')}]: ").strip()
        if email:
            student["email"] = email
        
        phone = input(f"New Phone [{student.get('phone', '')}]: ").strip()
        if phone:
            student["phone"] = phone
        
        save_students(students)
        print("\n✅ Student updated successfully!")
        
    except ValueError:
        print("❌ Invalid input type!")
    except Exception as e:
        print(f"❌ Error: {e}")


def delete_student(students):
    """Delete a student record."""
    print("\n--- Delete Student ---")
    sid = input("Enter Student ID to delete: ").strip().upper()
    
    for i, s in enumerate(students):
        if s["id"].upper() == sid:
            confirm = input(f"Are you sure you want to delete '{s['name']}'? (yes/no): ").strip().lower()
            if confirm in ["yes", "y"]:
                students.pop(i)
                save_students(students)
                print("✅ Student deleted successfully!")
            else:
                print("Cancelled.")
            return
    
    print("❌ Student not found!")


def sort_students(students):
    """Sort students by name or marks."""
    print("\n--- Sort Students ---")
    print("1. Sort by Name (A-Z)")
    print("2. Sort by Marks (High to Low)")
    print("3. Sort by Marks (Low to High)")
    
    try:
        choice = int(input("Choice: ").strip())
        
        if choice == 1:
            sorted_list = sorted(students, key=lambda x: x["name"].lower())
            display_students(sorted_list, "Sorted by Name (A-Z)")
        elif choice == 2:
            sorted_list = sorted(students, key=lambda x: x["marks"], reverse=True)
            display_students(sorted_list, "Sorted by Marks (High → Low)")
        elif choice == 3:
            sorted_list = sorted(students, key=lambda x: x["marks"])
            display_students(sorted_list, "Sorted by Marks (Low → High)")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a number!")


# ============================================================
# REPORTS
# ============================================================

def generate_reports(students):
    """Generate various reports."""
    if not students:
        print("\n📭 No data available for reports.")
        return
    
    print("\n" + "=" * 50)
    print("              REPORTS")
    print("=" * 50)
    
    # Total students
    print(f"\n📊 Total Students: {len(students)}")
    
    # Average marks
    avg = sum(s["marks"] for s in students) / len(students)
    print(f"📈 Average Marks: {avg:.2f}")
    
    # Topper
    topper = max(students, key=lambda x: x["marks"])
    print(f"🏆 Topper: {topper['name']} ({topper['marks']} marks) - {topper['course']}")
    
    # Lowest
    lowest = min(students, key=lambda x: x["marks"])
    print(f"📉 Lowest: {lowest['name']} ({lowest['marks']} marks)")
    
    # Course-wise count
    print("\n📚 Course-wise Distribution:")
    courses = {}
    for s in students:
        courses[s["course"]] = courses.get(s["course"], 0) + 1
    for course, count in courses.items():
        print(f"   {course}: {count} students")
    
    # Pass/Fail (assuming 40 is pass)
    passed = len([s for s in students if s["marks"] >= 40])
    failed = len(students) - passed
    print(f"\n✅ Passed (≥40): {passed}")
    print(f"❌ Failed (<40): {failed}")
    
    # Grade distribution
    print("\n🎓 Grade Distribution:")
    grades = {"A (90+)": 0, "B (75-89)": 0, "C (60-74)": 0, "D (40-59)": 0, "F (<40)": 0}
    for s in students:
        m = s["marks"]
        if m >= 90:
            grades["A (90+)"] += 1
        elif m >= 75:
            grades["B (75-89)"] += 1
        elif m >= 60:
            grades["C (60-74)"] += 1
        elif m >= 40:
            grades["D (40-59)"] += 1
        else:
            grades["F (<40)"] += 1
    for g, c in grades.items():
        print(f"   {g}: {c}")
    
    print("=" * 50)


# ============================================================
# MAIN MENU
# ============================================================

def main():
    """Main function."""
    print("\n" + "█" * 50)
    print("█" + " " * 48 + "█")
    print("█" + "   STUDENT MANAGEMENT SYSTEM".center(48) + "█")
    print("█" + "   MCA III Semester Project".center(48) + "█")
    print("█" + " " * 48 + "█")
    print("█" * 50)
    
    # Login required
    if not admin_login():
        return
    
    students = load_students()
    
    while True:
        print("\n" + "─" * 40)
        print("           MAIN MENU")
        print("─" * 40)
        print("  1. Add Student")
        print("  2. Display All Students")
        print("  3. Search Student")
        print("  4. Update Student")
        print("  5. Delete Student")
        print("  6. Sort Students")
        print("  7. Generate Reports")
        print("  8. Exit")
        print("─" * 40)
        
        try:
            choice = int(input("Enter your choice (1-8): ").strip())
        except ValueError:
            print("❌ Please enter a valid number!")
            continue
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        
        if choice == 1:
            add_student(students)
        elif choice == 2:
            display_students(students)
        elif choice == 3:
            search_student(students)
        elif choice == 4:
            update_student(students)
        elif choice == 5:
            delete_student(students)
        elif choice == 6:
            sort_students(students)
        elif choice == 7:
            generate_reports(students)
        elif choice == 8:
            print("\nThank you for using Student Management System! 👋")
            break
        else:
            print("❌ Invalid choice! Please select 1-8.")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}")
