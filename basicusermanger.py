from typing import List
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class User:
    def __init__(self, name: str, email: str, role: Role = Role.USER):
        self.name = name
        self.email = email
        self.role = role

    def __str__(self):
        return f"👤 {self.name} | 📧 {self.email} | 🏷️ {self.role.value}"


class UserManager:
    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User):
        if not any(u.email == user.email for u in self.users):
            self.users.append(user)
            return True
        print(f"⚠️ Email {user.email} already registered")
        return False

    def remove_user(self, admin: User, email: str):
        if admin.role == Role.ADMIN:
            for user in self.users[:]:
                if user.email == email:
                    self.users.remove(user)
                    return True
        return False

    def change_role(self, admin: User, email: str, new_role: Role):
        if admin.role == Role.ADMIN:
            for user in self.users:
                if user.email == email:
                    user.role = new_role
                    return True
        return False

    def show_users(self, requester: User):
        if requester.role == Role.ADMIN:
            print("\n👥 All Users:")
            for user in self.users:
                print(user)
        else:
            print("\n🔒 Unauthorized: Only admins can view all users")


def main():
    admin = User("Admin", "admin@example.com", Role.ADMIN)
    user1 = User("Mahdi", "mahdi@example.com")
    user2 = User("Ali", "ali@example.com")

    manager = UserManager()
    manager.add_user(admin)
    manager.add_user(user1)
    manager.add_user(user2)

    print("\nAdmin View:")
    manager.show_users(admin)

    print("\nUser View:")
    manager.show_users(user1)

    manager.change_role(admin, "mahdi@example.com", Role.ADMIN)
    print("\nAfter Role Change:")
    manager.show_users(admin)


if __name__ == '__main__':
    main()