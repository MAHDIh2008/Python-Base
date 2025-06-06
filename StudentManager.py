import json
import os
from typing import Dict, List

class Student:
    def __init__(self, name: str):
        self.name = name
        self.grades: List[float] = []

    def add_grade(self, grade: float):
        if 0 <= grade <= 20:
            self.grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 20")

    def average(self) -> float:
        return round(sum(self.grades) / len(self.grades), 2) if self.grades else 0.0

    def to_dict(self) -> Dict:
        return {'name': self.name, 'grades': self.grades}

    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        student = cls(data['name'])
        student.grades = data['grades']
        return student

class StudentManager:
    FILE = 'students.json'
    students: Dict[str, Student] = {}

    @classmethod
    def _save_to_file(cls):
        try:
            with open(cls.FILE, 'w') as f:
                json.dump({name: s.to_dict() for name, s in cls.students.items()}, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    @classmethod
    def _load_from_file(cls):
        if os.path.exists(cls.FILE):
            try:
                with open(cls.FILE, 'r') as f:
                    data = json.load(f)
                    cls.students = {name: Student.from_dict(s_data) for name, s_data in data.items()}
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading data: {e}")

    @classmethod
    def add_student(cls):
        name = input("Student name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        if name in cls.students:
            print("Student already exists!")
        else:
            cls.students[name] = Student(name)
            cls._save_to_file()
            print(f"Student {name} added successfully.")

    @classmethod
    def add_grade(cls):
        name = input("Student name: ").strip()
        if name not in cls.students:
            print("Student not found!")
            return
        try:
            grade = float(input("Grade (0-20): "))
            cls.students[name].add_grade(grade)
            cls._save_to_file()
            print("Grade added successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    @classmethod
    def show_students(cls):
        if not cls.students:
            print("No students available.")
            return
        print("\nStudent List:")
        print("-" * 40)
        for name, student in cls.students.items():
            avg = student.average()
            print(f"{name:<20} | Grades: {student.grades} | Average: {avg}")

    @classmethod
    def show_average(cls):
        name = input("Student name: ").strip()
        if name in cls.students:
            avg = cls.students[name].average()
            print(f"Average for {name}: {avg}")
        else:
            print("Student not found!")

def main():
    StudentManager._load_from_file()
    menu = {
        '1': ('Add Student', StudentManager.add_student),
        '2': ('Add Grade', StudentManager.add_grade),
        '3': ('View All Students', StudentManager.show_students),
        '4': ('View Student Average', StudentManager.show_average),
        '5': ('Exit', None)
    }

    while True:
        print("\nStudent Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
        
        choice = input("\nEnter your choice (1-5): ")
        if choice == '5':
            print("Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()