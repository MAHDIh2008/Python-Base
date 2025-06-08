from typing import List
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class User:
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role

    def __str__(self):
        return f"👤 {self.name} | 🏷️ {self.role.value}"


class UserManager:
    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User):
        if not any(u.name == user.name for u in self.users):
            self.users.append(user)
            return True
        print(f"⚠️ User {user.name} already exists")
        return False

    def update_role(self, username: str, new_role: Role):
        for user in self.users:
            if user.name == username:
                user.role = new_role
                return True
        return False

    def show_users(self, role: Role = None):
        users = [u for u in self.users if u.role == role] if role else self.users
        print("\n👥 Users:")
        if not users:
            print("No users found")
        for user in users:
            print(user)


def main():
    manager = UserManager()

    users = [
        User("Admin", Role.ADMIN),
        User("Editor", Role.EDITOR),
        User("Viewer", Role.VIEWER)
    ]

    for user in users:
        manager.add_user(user)

    print("\nAll Users:")
    manager.show_users()

    print("\nAdmins Only:")
    manager.show_users(Role.ADMIN)

    manager.update_role("Editor", Role.ADMIN)
    print("\nAfter Promotion:")
    manager.show_users()


if __name__ == '__main__':
    main()