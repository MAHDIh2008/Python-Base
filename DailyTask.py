import json
from datetime import datetime
from typing import Dict, List

class Task:
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.completed = False

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} - {self.description}"

class DailyTaskManager:
    FILE = 'daily_tasks.json'
    tasks: Dict[str, List[Task]] = {}

    @classmethod
    def _validate_date(cls, date_str: str) -> str:
        try:
            datetime.strptime(date_str, "%Y/%m/%d")
            return date_str
        except ValueError:
            raise ValueError("Invalid date format (YYYY/MM/DD)")

    @classmethod
    def add_task(cls):
        try:
            date = cls._validate_date(input("Date (YYYY/MM/DD): ").strip())
            title = input("Title: ").strip()
            if not title:
                raise ValueError("Title cannot be empty")
                
            description = input("Description: ").strip()
            cls.tasks.setdefault(date, []).append(Task(title, description))
            print("✅ Task added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def show_tasks(cls):
        date = input("Date (YYYY/MM/DD): ").strip()
        try:
            date = cls._validate_date(date)
            tasks = cls.tasks.get(date, [])
            
            if not tasks:
                print(f"📅 No tasks for {date}")
                return
                
            print(f"\n📅 Tasks for {date}:")
            print("-" * 60)
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def delete_task(cls):
        date = input("Date (YYYY/MM/DD): ").strip()
        try:
            date = cls._validate_date(date)
            if date not in cls.tasks or not cls.tasks[date]:
                print(f"❌ No tasks for {date}")
                return
                
            cls.show_tasks()
            try:
                task_num = int(input("Task number to delete: ")) - 1
                if 0 <= task_num < len(cls.tasks[date]):
                    deleted = cls.tasks[date].pop(task_num)
                    print(f"✅ Deleted: {deleted.title}")
                    if not cls.tasks[date]:
                        del cls.tasks[date]
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def toggle_completion(cls):
        date = input("Date (YYYY/MM/DD): ").strip()
        try:
            date = cls._validate_date(date)
            if date not in cls.tasks or not cls.tasks[date]:
                print(f"❌ No tasks for {date}")
                return
                
            cls.show_tasks()
            try:
                task_num = int(input("Task number to toggle: ")) - 1
                if 0 <= task_num < len(cls.tasks[date]):
                    task = cls.tasks[date][task_num]
                    task.completed = not task.completed
                    status = "completed" if task.completed else "pending"
                    print(f"✅ Task marked as {status}")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def show_summary(cls):
        if not cls.tasks:
            print("📅 No tasks available")
            return
            
        print("\n📅 Task Summary:")
        print("-" * 40)
        for date in sorted(cls.tasks.keys()):
            total = len(cls.tasks[date])
            completed = sum(1 for t in cls.tasks[date] if t.completed)
            print(f"{date}: {completed}/{total} tasks completed")

    @classmethod
    def save_to_file(cls):
        try:
            data = {
                date: [
                    {
                        'title': task.title,
                        'description': task.description,
                        'completed': task.completed,
                        'created_at': task.created_at.isoformat()
                    }
                    for task in tasks
                ]
                for date, tasks in cls.tasks.items()
            }
            
            with open(cls.FILE, 'w') as file:
                json.dump(data, file, indent=2)
            print("💾 Tasks saved successfully!")
        except IOError as e:
            print(f"❌ Error saving tasks: {e}")

    @classmethod
    def load_from_file(cls):
        try:
            with open(cls.FILE, 'r') as file:
                data = json.load(file)
                cls.tasks = {
                    date: [
                        Task(
                            task['title'],
                            task['description']
                        )
                        for task in tasks
                    ]
                    for date, tasks in data.items()
                }
                
                # Restore completion status and creation time
                for date, tasks in data.items():
                    for i, task_data in enumerate(tasks):
                        cls.tasks[date][i].completed = task_data['completed']
                        cls.tasks[date][i].created_at = datetime.fromisoformat(task_data['created_at'])
        except FileNotFoundError:
            print("ℹ️ No existing task file found")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Error loading tasks: {e}")

def main():
    DailyTaskManager.load_from_file()
    
    menu = {
        '1': ('Add Task', DailyTaskManager.add_task),
        '2': ('View Tasks', DailyTaskManager.show_tasks),
        '3': ('Delete Task', DailyTaskManager.delete_task),
        '4': ('Toggle Completion', DailyTaskManager.toggle_completion),
        '5': ('Task Summary', DailyTaskManager.show_summary),
        '6': ('Save', DailyTaskManager.save_to_file),
        '7': ('Exit', None)
    }

    while True:
        print("\n📅 Daily Task Manager")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-7): ")
        if choice == '7':
            DailyTaskManager.save_to_file()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()