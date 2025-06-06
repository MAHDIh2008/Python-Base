import csv
import os
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Customer:
    name: str
    renewal: str = "Not yet"
    done: bool = False

class QueueManager:
    FILE = 'queue.csv'
    customers: List[Customer] = []

    @classmethod
    def load_queue(cls):
        if os.path.exists(cls.FILE):
            try:
                with open(cls.FILE, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    cls.customers = [
                        Customer(
                            row['name'],
                            row['renewal'],
                            row['done'].lower() == 'true'
                        )
                        for row in reader
                        if row['name']
                    ]
            except Exception as e:
                print(f"❌ Error loading queue: {e}")

    @classmethod
    def save_queue(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'renewal', 'done'])
                writer.writeheader()
                for customer in cls.customers:
                    writer.writerow({
                        'name': customer.name,
                        'renewal': customer.renewal,
                        'done': str(customer.done)
                    })
        except Exception as e:
            print(f"❌ Error saving queue: {e}")

    @classmethod
    def add_customer(cls):
        name = input("Customer name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
            
        cls.customers.append(Customer(name))
        cls.save_queue()
        print(f"✅ Added {name} to the queue")

    @classmethod
    def show_queue(cls):
        if not cls.customers:
            print("📭 Queue is empty")
            return
            
        print("\n📋 Current Queue:")
        print("=" * 60)
        for idx, customer in enumerate(cls.customers, 1):
            status = "✓" if customer.done else "✗"
            print(f"{idx}. {customer.name} | Renewal: {customer.renewal} | Status: {status}")

    @classmethod
    def process_queue(cls):
        if not cls.customers:
            print("📭 Queue is empty")
            return
            
        print("\n🔄 Processing Queue:")
        for customer in cls.customers[:]:
            if not customer.done:
                print(f"\nCurrent customer: {customer.name}")
                action = input("Enter 's' to skip, 'd' to mark done, or 'x' to exit: ").lower()
                
                if action == 'x':
                    break
                elif action == 'd':
                    customer.renewal = input("Enter renewal details: ").strip()
                    customer.done = True
                    print(f"✅ Completed: {customer.name}")
                elif action == 's':
                    print(f"⏭ Skipped: {customer.name}")
                    continue
                    
        cls.save_queue()
        print("\nQueue processing complete")

    @classmethod
    def customer_inquiry(cls):
        name = input("Search customer name: ").strip()
        for customer in cls.customers:
            if customer.name.lower() == name.lower():
                print(f"\n🔍 Customer Found:")
                print(f"Name: {customer.name}")
                print(f"Renewal: {customer.renewal}")
                print(f"Status: {'Done' if customer.done else 'Pending'}")
                return
        print("❌ Customer not found")

def main():
    QueueManager.load_queue()
    
    menu = {
        '1': ('Add Customer', QueueManager.add_customer),
        '2': ('View Queue', QueueManager.show_queue),
        '3': ('Process Queue', QueueManager.process_queue),
        '4': ('Customer Inquiry', QueueManager.customer_inquiry),
        '5': ('Exit', None)
    }

    while True:
        print("\n📞 Queue Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-5): ")
        if choice == '5':
            QueueManager.save_queue()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()