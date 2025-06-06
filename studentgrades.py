import csv
import os
from typing import Dict

class GradeManager:
    FILE = 'grades.csv'
    grades: Dict[str, float] = {}

    @classmethod
    def load_grades(cls):
        if os.path.exists(cls.FILE):
            try:
                with open(cls.FILE, 'r', newline='') as file:
                    reader = csv.reader(file)
                    cls.grades = {
                        row[0]: float(row[1])
                        for row in reader if len(row) >= 2 and row[0]
                    }
            except Exception as e:
                print(f"❌ Error loading grades: {e}")

    @classmethod
    def save_grades(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                for name, grade in cls.grades.items():
                    writer.writerow([name, grade])
        except Exception as e:
            print(f"❌ Error saving grades: {e}")

    @classmethod
    def add_student(cls):
        try:
            name = input("Student name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty")
                
            if name in cls.grades:
                print("⚠️ Student already exists!")
                return
                
            grade = float(input("Grade (0-20): ").strip())
            if not 0 <= grade <= 20:
                raise ValueError("Grade must be between 0-20")
                
            cls.grades[name] = grade
            cls.save_grades()
            print("✅ Student added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def edit_grade(cls):
        name = input("Student name: ").strip()
        if name not in cls.grades:
            print("❌ Student not found!")
            return
            
        try:
            new_grade = float(input("New grade (0-20): ").strip())
            if not 0 <= new_grade <= 20:
                raise ValueError("Grade must be between 0-20")
                
            cls.grades[name] = new_grade
            cls.save_grades()
            print("✅ Grade updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def delete_student(cls):
        name = input("Student name to delete: ").strip()
        if name in cls.grades:
            confirm = input(f"Delete {name}? (y/n): ").lower()
            if confirm == 'y':
                del cls.grades[name]
                cls.save_grades()
                print("✅ Student deleted successfully!")
        else:
            print("❌ Student not found!")

    @classmethod
    def search_student(cls):
        name = input("Search student name: ").strip().lower()
        results = {
            n: g for n, g in cls.grades.items()
            if name in n.lower()
        }
        
        if not results:
            print("❌ No matching students found")
            return
            
        print("\n🔍 Search Results:")
        for name, grade in results.items():
            print(f"{name}: {grade:.2f}")

    @classmethod
    def show_all(cls):
        if not cls.grades:
            print("📭 No students in records")
            return
            
        print("\n📊 All Students:")
        print("=" * 40)
        for name, grade in sorted(cls.grades.items()):
            print(f"{name:<20}: {grade:.2f}")

    @classmethod
    def show_stats(cls):
        if not cls.grades:
            print("📭 No students in records")
            return
            
        grades = cls.grades.values()
        average = sum(grades) / len(grades)
        highest = max(grades)
        lowest = min(grades)
        
        print("\n📈 Grade Statistics:")
        print(f"Average: {average:.2f}")
        print(f"Highest: {highest:.2f}")
        print(f"Lowest: {lowest:.2f}")

def main():
    GradeManager.load_grades()
    
    menu = {
        '1': ('Add Student', GradeManager.add_student),
        '2': ('Edit Grade', GradeManager.edit_grade),
        '3': ('Delete Student', GradeManager.delete_student),
        '4': ('Search Student', GradeManager.search_student),
        '5': ('View All', GradeManager.show_all),
        '6': ('View Stats', GradeManager.show_stats),
        '7': ('Exit', None)
    }

    while True:
        print("\n📝 Grade Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-7): ")
        if choice == '7':
            GradeManager.save_grades()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()