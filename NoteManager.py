import csv
import os
from typing import Dict, Optional

class Note:
    def __init__(self, title: str, content: str):
        self.title = title.strip()
        self.content = content.strip()

    def __str__(self):
        return f"📝 {self.title}\n{'-'*40}\n{self.content}"

class NoteManager:
    FILE = 'notes.csv'
    notes: Dict[str, str] = {}

    @classmethod
    def load_notes(cls):
        if os.path.exists(cls.FILE):
            try:
                with open(cls.FILE, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    cls.notes = {title: content for title, content in reader}
            except Exception as e:
                print(f"❌ Error loading notes: {e}")

    @classmethod
    def save_notes(cls):
        try:
            with open(cls.FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for title, content in cls.notes.items():
                    writer.writerow([title, content])
        except Exception as e:
            print(f"❌ Error saving notes: {e}")

    @classmethod
    def add_note(cls):
        try:
            title = input("Note title: ").strip()
            if not title:
                raise ValueError("Title cannot be empty")
                
            if title in cls.notes:
                print("⚠️ Note with this title already exists!")
                return
                
            content = input("Note content: ").strip()
            if not content:
                raise ValueError("Content cannot be empty")
                
            cls.notes[title] = content
            cls.save_notes()
            print("✅ Note added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def show_notes(cls):
        if not cls.notes:
            print("📭 No notes available")
            return
            
        print("\n📒 Your Notes:")
        print("=" * 60)
        for idx, (title, content) in enumerate(cls.notes.items(), 1):
            print(f"{idx}. {Note(title, content)}")
            print("=" * 60)

    @classmethod
    def delete_note(cls):
        cls.show_notes()
        if not cls.notes:
            return
            
        try:
            choice = input("Enter note title to delete (or 'cancel'): ").strip()
            if choice.lower() == 'cancel':
                return
                
            if choice in cls.notes:
                confirm = input(f"Delete '{choice}'? (y/n): ").lower()
                if confirm == 'y':
                    del cls.notes[choice]
                    cls.save_notes()
                    print("✅ Note deleted successfully!")
            else:
                print("❌ Note not found!")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    NoteManager.load_notes()
    
    menu = {
        '1': ('Add Note', NoteManager.add_note),
        '2': ('View Notes', NoteManager.show_notes),
        '3': ('Delete Note', NoteManager.delete_note),
        '4': ('Exit', None)
    }

    while True:
        print("\n📝 Note Manager")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-4): ")
        if choice == '4':
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()