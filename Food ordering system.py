import csv
import os
from typing import Dict, List

class MenuItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

class Menu:
    FILE = 'menu.csv'
    items: Dict[str, MenuItem] = {}

    @classmethod
    def load_menu(cls):
        try:
            with open(cls.FILE, 'r', newline='') as file:
                reader = csv.DictReader(file)
                cls.items = {
                    row['name']: MenuItem(row['name'], float(row['price']))
                    for row in reader if row['name'] and row['price']
                }
        except FileNotFoundError:
            print("ℹ️ No menu file found. Starting with empty menu.")
        except Exception as e:
            print(f"❌ Error loading menu: {e}")

    @classmethod
    def show_menu(cls):
        if not cls.items:
            print("📭 The menu is empty!")
            return
            
        print("\n🍽️  Menu:")
        print("=" * 40)
        for idx, (name, item) in enumerate(cls.items.items(), 1):
            print(f"{idx}. {item}")

    @classmethod
    def add_item(cls):
        try:
            name = input("Item name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty")
                
            price = float(input("Price: $").strip())
            if price <= 0:
                raise ValueError("Price must be positive")
                
            cls.items[name] = MenuItem(name, price)
            cls.save_menu()
            print("✅ Item added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def save_menu(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'price'])
                writer.writeheader()
                for item in cls.items.values():
                    writer.writerow({'name': item.name, 'price': item.price})
        except Exception as e:
            print(f"❌ Error saving menu: {e}")

class Order:
    FILE = 'orders.csv'
    
    def __init__(self):
        self.items: Dict[str, int] = {}
        self.load_orders()

    def load_orders(self):
        if os.path.exists(self.FILE):
            try:
                with open(self.FILE, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.items[row['item']] = self.items.get(row['item'], 0) + 1
            except Exception as e:
                print(f"❌ Error loading orders: {e}")

    def save_orders(self):
        try:
            with open(self.FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['item', 'price'])
                writer.writeheader()
                for item, count in self.items.items():
                    if item in Menu.items:
                        writer.writerow({
                            'item': item,
                            'price': Menu.items[item].price
                        })
        except Exception as e:
            print(f"❌ Error saving orders: {e}")

    def add_item(self, item_name: str):
        if item_name not in Menu.items:
            print(f"❌ {item_name} is not in the menu!")
            return
            
        self.items[item_name] = self.items.get(item_name, 0) + 1
        self.save_orders()
        print(f"✅ Added {item_name} to your order")

    def remove_item(self, item_name: str):
        if item_name not in self.items:
            print(f"❌ {item_name} is not in your order!")
            return
            
        self.items[item_name] -= 1
        if self.items[item_name] <= 0:
            del self.items[item_name]
        self.save_orders()
        print(f"✅ Removed {item_name} from your order")

    def show_order(self):
        if not self.items:
            print("🛒 Your order is empty!")
            return
            
        total = 0.0
        print("\n🛒 Your Order:")
        print("=" * 40)
        for item, count in self.items.items():
            item_total = Menu.items[item].price * count
            print(f"{item} x{count}: ${item_total:.2f}")
            total += item_total
        print("=" * 40)
        print(f"💵 TOTAL: ${total:.2f}")

def main():
    Menu.load_menu()
    order = Order()
    
    while True:
        print("\n🍕 Restaurant Order System")
        print("=" * 30)
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Add to Order")
        print("4. Remove from Order")
        print("5. View Order")
        print("6. Checkout")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ")
        
        if choice == '1':
            Menu.show_menu()
            
        elif choice == '2':
            Menu.add_item()
            
        elif choice == '3':
            Menu.show_menu()
            item = input("Enter item name: ").strip()
            order.add_item(item)
            
        elif choice == '4':
            order.show_order()
            item = input("Enter item to remove: ").strip()
            order.remove_item(item)
            
        elif choice == '5':
            order.show_order()
            
        elif choice == '6':
            order.show_order()
            if order.items:
                confirm = input("Confirm order? (y/n): ").lower()
                if confirm == 'y':
                    print("🍽️  Order placed! Thank you!")
                    order.items.clear()
                    order.save_orders()
                    
        elif choice == '7':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()