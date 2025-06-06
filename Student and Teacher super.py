from typing import Optional
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

    def info(self):
        print(f"👤 Name: {self.name} | Age: {self.age}")

class Student(Person):
    def __init__(self, name: str, age: int, grade: float):
        super().__init__(name, age)
        self.grade = grade

    def info(self):
        super().info()
        print(f"📊 Grade: {self.grade}")

    @classmethod
    def create_from_input(cls) -> Optional['Student']:
        try:
            name = input("Student name: ").strip()
            age = int(input("Age: "))
            grade = float(input("Grade (0-20): "))
            if not 0 <= grade <= 20:
                raise ValueError("Grade must be between 0-20")
            return cls(name, age, grade)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None

class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str):
        super().__init__(name, age)
        self.subject = subject

    def info(self):
        super().info()
        print(f"📚 Subject: {self.subject}")

    @classmethod
    def create_from_input(cls) -> Optional['Teacher']:
        try:
            name = input("Teacher name: ").strip()
            age = int(input("Age: "))
            subject = input("Subject: ").strip()
            if not all([name, subject]):
                raise ValueError("Name and subject cannot be empty")
            return cls(name, age, subject)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None

def main():
    people = []
    
    # Sample data
    people.append(Student("Mahdi", 17, 18.5))
    people.append(Teacher("Dr. Smith", 45, "Mathematics"))
    
    while True:
        print("\n👥 People Management System")
        print("=" * 30)
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. View All")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            student = Student.create_from_input()
            if student:
                people.append(student)
                print("✅ Student added successfully!")
                
        elif choice == '2':
            teacher = Teacher.create_from_input()
            if teacher:
                people.append(teacher)
                print("✅ Teacher added successfully!")
                
        elif choice == '3':
            if not people:
                print("📭 No people registered")
                continue
                
            print("\n👥 People List:")
            print("-" * 40)
            for person in people:
                person.info()
                print("-" * 40)
                
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()