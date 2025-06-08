from typing import List


class Teacher:
    def __init__(self, name: str, age: int, code: str):
        self.name = name
        self.age = age
        self.code = code

    def __str__(self):
        return f"👨‍🏫 {self.name} ({self.code}) | Age: {self.age}"


class Student:
    def __init__(self, name: str, age: int, code: str):
        self.name = name
        self.age = age
        self.code = code

    def __str__(self):
        return f"👨‍🎓 {self.name} ({self.code}) | Age: {self.age}"


class Course:
    def __init__(self, title: str, instructor: Teacher):
        self.title = title
        self.instructor = instructor
        self.students: List[Student] = []

    def enroll_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            return True
        print(f"⚠️ {student.name} is already enrolled")
        return False

    def show_info(self):
        print(f"\n📚 Course: {self.title}")
        print(f"Instructor: {self.instructor}")
        print("\nStudents:")
        if not self.students:
            print("No students enrolled")
        for student in self.students:
            print(student)


class CourseManager:
    def __init__(self):
        self.courses: List[Course] = []

    def add_course(self, course: Course):
        self.courses.append(course)

    def enroll_student(self, course_title: str, student: Student):
        for course in self.courses:
            if course.title == course_title:
                return course.enroll_student(student)
        print(f"⚠️ Course {course_title} not found")
        return False

    def show_courses(self):
        print("\n📂 All Courses:")
        for course in self.courses:
            course.show_info()


def main():
    manager = CourseManager()

    teachers = [
        Teacher("Dr. Smith", 45, "T001"),
        Teacher("Prof. Johnson", 50, "T002")
    ]

    students = [
        Student("Alice", 20, "S001"),
        Student("Bob", 21, "S002")
    ]

    courses = [
        Course("Python Programming", teachers[0]),
        Course("Web Development", teachers[1])
    ]

    for course in courses:
        manager.add_course(course)

    manager.enroll_student("Python Programming", students[0])
    manager.enroll_student("Web Development", students[1])
    manager.enroll_student("Web Development", students[0])

    manager.show_courses()


if __name__ == '__main__':
    main()