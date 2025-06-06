import csv
import json
import os
from typing import Dict, List

class Student:
    def __init__(self, name: str, student_id: str):
        self.name = name.strip()
        self.student_id = student_id.strip()

    def __str__(self):
        return f"🎓 {self.name} (ID: {self.student_id})"

class Course:
    def __init__(self, name: str, code: str, capacity: int):
        self.name = name.strip()
        self.code = code.strip()
        self.capacity = capacity
        self.students: List[str] = []

    def add_student(self, student_id: str) -> bool:
        if len(self.students) < self.capacity and student_id not in self.students:
            self.students.append(student_id)
            return True
        return False

    def __str__(self):
        return f"📚 {self.name} ({self.code}) - {len(self.students)}/{self.capacity} students"

class RegistrationSystem:
    STUDENT_FILE = 'students.csv'
    COURSE_FILE = 'courses.json'
    
    students: Dict[str, Student] = {}
    courses: Dict[str, Dict[str, Course]] = {}

    @classmethod
    def load_data(cls):
        # Load students
        if os.path.exists(cls.STUDENT_FILE):
            with open(cls.STUDENT_FILE, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.students = {
                    row[1]: Student(row[0], row[1])
                    for row in reader if len(row) >= 2
                }

        # Load courses
        if os.path.exists(cls.COURSE_FILE):
            try:
                with open(cls.COURSE_FILE, 'r') as file:
                    data = json.load(file)
                    for course_name, courses in data.items():
                        cls.courses[course_name] = {}
                        for code, details in courses.items():
                            course = Course(course_name, code, details['capacity'])
                            course.students = details['students']
                            cls.courses[course_name][code] = course
            except Exception as e:
                print(f"❌ Error loading courses: {e}")

    @classmethod
    def save_data(cls):
        # Save students
        with open(cls.STUDENT_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            for student in cls.students.values():
                writer.writerow([student.name, student.student_id])

        # Save courses
        courses_data = {
            course_name: {
                code: {
                    'capacity': course.capacity,
                    'students': course.students
                }
                for code, course in courses.items()
            }
            for course_name, courses in cls.courses.items()
        }
        
        with open(cls.COURSE_FILE, 'w') as file:
            json.dump(courses_data, file, indent=2)

    @classmethod
    def register_student(cls):
        try:
            name = input("Student name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty")
                
            student_id = input("Student ID: ").strip()
            if not student_id:
                raise ValueError("ID cannot be empty")
                
            if student_id in cls.students:
                print("⚠️ Student ID already exists!")
                return
                
            cls.students[student_id] = Student(name, student_id)
            cls.save_data()
            print("✅ Student registered successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def add_course(cls):
        try:
            name = input("Course name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty")
                
            code = input("Course code: ").strip()
            if not code:
                raise ValueError("Code cannot be empty")
                
            capacity = int(input("Capacity: ").strip())
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
                
            if name not in cls.courses:
                cls.courses[name] = {}
                
            if code in cls.courses[name]:
                print("⚠️ Course code already exists!")
                return
                
            cls.courses[name][code] = Course(name, code, capacity)
            cls.save_data()
            print("✅ Course added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def enroll_student(cls):
        student_id = input("Student ID: ").strip()
        if student_id not in cls.students:
            print("❌ Student not found!")
            return
            
        course_name = input("Course name: ").strip()
        if course_name not in cls.courses:
            print("❌ Course not found!")
            return
            
        course_code = input("Course code: ").strip()
        if course_code not in cls.courses[course_name]:
            print("❌ Class not found!")
            return
            
        course = cls.courses[course_name][course_code]
        if course.add_student(student_id):
            cls.save_data()
            print(f"✅ Enrolled {cls.students[student_id].name} in {course.name} ({course.code})")
        else:
            print("❌ Enrollment failed (class full or already enrolled)")

    @classmethod
    def search_student(cls):
        query = input("Search by name or ID: ").strip().lower()
        results = [
            student for student in cls.students.values()
            if query in student.name.lower() or query in student.student_id.lower()
        ]
        
        if not results:
            print("❌ No matching students found")
            return
            
        print("\n🔍 Search Results:")
        for student in results:
            print(student)
            # Find enrolled courses
            enrolled = []
            for course_name, courses in cls.courses.items():
                for course in courses.values():
                    if student.student_id in course.students:
                        enrolled.append(f"{course_name} ({course.code})")
            
            if enrolled:
                print("   Enrolled in:", ", ".join(enrolled))
            else:
                print("   Not enrolled in any courses")
            print("-" * 40)

    @classmethod
    def show_courses(cls):
        if not cls.courses:
            print("📭 No courses available")
            return
            
        print("\n📚 Course Catalog:")
        for course_name, courses in cls.courses.items():
            print(f"\n{course_name}:")
            print("-" * 40)
            for course in courses.values():
                print(course)

def main():
    RegistrationSystem.load_data()
    
    menu = {
        '1': ('Register Student', RegistrationSystem.register_student),
        '2': ('Add Course', RegistrationSystem.add_course),
        '3': ('Enroll Student', RegistrationSystem.enroll_student),
        '4': ('Search Student', RegistrationSystem.search_student),
        '5': ('View Courses', RegistrationSystem.show_courses),
        '6': ('Exit', None)
    }

    while True:
        print("\n🎓 Student Registration System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-6): ")
        if choice == '6':
            RegistrationSystem.save_data()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()