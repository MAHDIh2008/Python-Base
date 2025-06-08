from typing import List
from enum import Enum, auto


class Status(Enum):
    PENDING = auto()
    INTERVIEWED = auto()
    REJECTED = auto()
    HIRED = auto()


class Applicant:
    def __init__(self, name: str, email: str, position: str):
        self.name = name
        self.email = email
        self.position = position
        self.status = Status.PENDING

    def __str__(self):
        return f"👤 {self.name} | 📧 {self.email} | 💼 {self.position} | 🏷️ {self.status.name}"


class HRManager:
    def __init__(self):
        self.applicants: List[Applicant] = []

    def add_applicant(self, applicant: Applicant):
        self.applicants.append(applicant)

    def update_status(self, email: str, status: Status):
        for applicant in self.applicants:
            if applicant.email == email:
                applicant.status = status
                return True
        return False

    def filter_by_status(self, status: Status):
        return [app for app in self.applicants if app.status == status]

    def show_applicants(self, status: Status = None):
        applicants = self.filter_by_status(status) if status else self.applicants
        print("\n📋 Applicants:")
        if not applicants:
            print("No applicants found")
        for applicant in applicants:
            print(applicant)


def main():
    hr = HRManager()

    applicants = [
        Applicant("Alice", "alice@example.com", "Developer"),
        Applicant("Bob", "bob@example.com", "Designer")
    ]

    for applicant in applicants:
        hr.add_applicant(applicant)

    hr.update_status("alice@example.com", Status.INTERVIEWED)
    hr.update_status("bob@example.com", Status.REJECTED)

    print("\nAll Applicants:")
    hr.show_applicants()

    print("\nInterviewed Applicants:")
    hr.show_applicants(Status.INTERVIEWED)


if __name__ == '__main__':
    main()