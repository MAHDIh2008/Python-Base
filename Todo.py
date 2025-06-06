from typing import List, Dict
from datetime import datetime

class Task:
    def __init__(self, title: str, description: str = "", due_date: str = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_done = False
        self.created_at = datetime.now()

    def mark_as_done(self):
        self.is_done = True

    def __str__(self):
        status = "✓" if self.is_done else "✗"
        due = f" | Due: {self.due_date}" if self.due_date else ""
        return f"[{status}] {self.title}{due} - {self.description}"

class TaskManager:
    tasks: List[Task] = []

    @classmethod
    def add_task(cls):
        title = input("Task title: ").strip()
        if not title:
            print("Title cannot be empty!")
            return
        description = input("Description: ").strip()
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
        cls.tasks.append(Task(title, description, due_date or None))
        print("Task added successfully!")

    @classmethod
    def show_tasks(cls):
        if not cls.tasks:
            print("No tasks available.")
            return
        print("\nTask List:")
        print("-" * 60)
        for idx, task in enumerate(cls.tasks, 1):
            print(f"{idx}. {task}")

    @classmethod
    def mark_done(cls):
        cls.show_tasks()
        if not cls.tasks:
            return
        try:
            choice = int(input("Select task number to mark as done: ")) - 1
            if 0 <= choice < len(cls.tasks):
                cls.tasks[choice].mark_as_done()
                print("Task marked as done!")
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a valid number!")

    @classmethod
    def delete_task(cls):
        cls.show_tasks()
        if not cls.tasks:
            return
        try:
            choice = int(input("Select task number to delete: ")) - 1
            if 0 <= choice < len(cls.tasks):
                deleted = cls.tasks.pop(choice)
                print(f"Deleted: {deleted.title}")
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a valid number!")

def main():
    menu = {
        '1': ('Add Task', TaskManager.add_task),
        '2': ('View Tasks', TaskManager.show_tasks),
        '3': ('Mark Task Done', TaskManager.mark_done),
        '4': ('Delete Task', TaskManager.delete_task),
        '5': ('Exit', None)
    }

    while True:
        print("\nTask Management System")
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