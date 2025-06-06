import csv
import os
from typing import Dict, Optional

class Contact:
    def __init__(self, name: str, phone: str, email: str = ""):
        self.name = name.lower().strip()
        self.phone = phone.strip()
        self.email = email.strip()

class ContactManager:
    FILE = "contacts.csv"
    FIELDS = ["name", "phone", "email"]

    @staticmethod
    def _load() -> Dict[str, Dict[str, str]]:
        contacts = {}
        if os.path.exists(ContactManager.FILE):
            try:
                with open(ContactManager.FILE, newline="", encoding='utf-8') as f:
                    reader = csv.DictReader(f, fieldnames=ContactManager.FIELDS)
                    for row in reader:
                        contacts[row['name']] = {
                            'phone': row['phone'],
                            'email': row['email']
                        }
            except (csv.Error, IOError) as e:
                print(f"⚠️ Error loading contacts: {str(e)}")
        return contacts

    @staticmethod
    def _save(contacts: Dict[str, Dict[str, str]]):
        try:
            with open(ContactManager.FILE, "w", newline="", encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=ContactManager.FIELDS)
                for name, info in contacts.items():
                    writer.writerow({
                        'name': name,
                        'phone': info['phone'],
                        'email': info['email']
                    })
        except IOError as e:
            print(f"⚠️ Error saving contacts: {str(e)}")

    @classmethod
    def _validate_phone(cls, phone: str) -> bool:
        return phone.isdigit() and len(phone) >= 10

    @classmethod
    def _validate_email(cls, email: str) -> bool:
        return '@' in email and '.' in email.split('@')[-1]

    @classmethod
    def add_contact(cls):
        try:
            name = input("Name: ").lower().strip()
            if not name:
                raise ValueError("Name cannot be empty")
                
            phone = input("Phone: ").strip()
            if not cls._validate_phone(phone):
                raise ValueError("Invalid phone number")
                
            email = input("Email (optional): ").strip()
            if email and not cls._validate_email(email):
                raise ValueError("Invalid email format")

            contacts = cls._load()
            if name in contacts:
                print("⚠️ Contact already exists!")
                return

            contacts[name] = {"phone": phone, "email": email}
            cls._save(contacts)
            print("✅ Contact added successfully!")
            
        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

    @classmethod
    def show_contacts(cls):
        contacts = cls._load()
        if not contacts:
            print("📭 No contacts available.")
            return
            
        print("\n📋 Contact List:")
        print("-" * 40)
        print(f"{'Name':<20} {'Phone':<15} {'Email':<25}")
        print("-" * 40)
        for name, info in sorted(contacts.items()):
            print(f"{name:<20} {info['phone']:<15} {info['email']:<25}")

    @classmethod
    def find_contact(cls):
        name = input("Search name: ").lower().strip()
        contacts = cls._load()
        contact = contacts.get(name)
        
        if contact:
            print("\n🔍 Contact Found:")
            print(f"Name: {name}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
        else:
            print("❌ Contact not found.")

    @classmethod
    def delete_contact(cls):
        name = input("Delete name: ").lower().strip()
        contacts = cls._load()
        
        if name in contacts:
            confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
            if confirm == 'y':
                del contacts[name]
                cls._save(contacts)
                print("✅ Contact deleted successfully!")
        else:
            print("❌ Contact not found.")

def main():
    manager = ContactManager()
    menu = {
        '1': ('Add Contact', manager.add_contact),
        '2': ('View All Contacts', manager.show_contacts),
        '3': ('Search Contact', manager.find_contact),
        '4': ('Delete Contact', manager.delete_contact),
        '5': ('Exit', exit)
    }

    while True:
        print("\n📞 Contact Manager")
        print("=" * 30)
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
            
        try:
            choice = input("\nEnter your choice (1-5): ")
            if choice == '5':
                print("👋 Goodbye!")
                break
                
            if choice in menu:
                menu[choice][1]()
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled.")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

if __name__ == '__main__':
    main()