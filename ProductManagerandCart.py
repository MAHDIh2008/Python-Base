import csv
from typing import List, Dict

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

class ProductManager:
    FILE = 'products.csv'
    products: List[Product] = []

    @classmethod
    def _validate_input(cls, name: str, price_str: str) -> float:
        if not name:
            raise ValueError("Product name cannot be empty")
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError("Price must be positive")
            return price
        except ValueError:
            raise ValueError("Invalid price format")

    @classmethod
    def add_product(cls):
        try:
            name = input("Product name: ").strip()
            price_str = input("Price: $").strip()
            price = cls._validate_input(name, price_str)
            
            cls.products.append(Product(name, price))
            cls.save_to_file()
            print("✅ Product added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def delete_product(cls):
        name = input("Product name to delete: ").strip()
        for product in cls.products[:]:
            if product.name.lower() == name.lower():
                cls.products.remove(product)
                cls.save_to_file()
                print("✅ Product deleted successfully!")
                return
        print("❌ Product not found!")

    @classmethod
    def show_products(cls):
        if not cls.products:
            print("📭 No products available")
            return
        print("\n🛍️  Product List:")
        print("-" * 40)
        for idx, product in enumerate(cls.products, 1):
            print(f"{idx}. {product}")

    @classmethod
    def save_to_file(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'price'])  # Header
                for product in cls.products:
                    writer.writerow([product.name, product.price])
        except IOError as e:
            print(f"❌ Error saving products: {e}")

    @classmethod
    def load_from_file(cls):
        try:
            with open(cls.FILE, 'r') as file:
                reader = csv.DictReader(file)
                cls.products = [
                    Product(row['name'], float(row['price']))
                    for row in reader if row['name'] and row['price']
                ]
        except FileNotFoundError:
            print("ℹ️ No existing product file found")
        except (ValueError, KeyError) as e:
            print(f"❌ Error loading products: {e}")

class Cart:
    FILE = 'cart.csv'
    items: List[Product] = []

    @classmethod
    def add_item(cls):
        ProductManager.show_products()
        if not ProductManager.products:
            return
            
        try:
            choice = int(input("Select product number: ")) - 1
            if 0 <= choice < len(ProductManager.products):
                cls.items.append(ProductManager.products[choice])
                cls.save_to_file()
                print("✅ Added to cart!")
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")

    @classmethod
    def remove_item(cls):
        if not cls.items:
            print("🛒 Your cart is empty!")
            return
            
        print("\n🛒 Your Cart:")
        for idx, item in enumerate(cls.items, 1):
            print(f"{idx}. {item}")
            
        try:
            choice = int(input("Select item to remove: ")) - 1
            if 0 <= choice < len(cls.items):
                removed = cls.items.pop(choice)
                cls.save_to_file()
                print(f"✅ Removed: {removed.name}")
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")

    @classmethod
    def show_cart(cls):
        if not cls.items:
            print("🛒 Your cart is empty!")
            return
            
        total = 0.0
        print("\n🛒 Your Shopping Cart:")
        print("-" * 40)
        for idx, item in enumerate(cls.items, 1):
            print(f"{idx}. {item}")
            total += item.price
        print("-" * 40)
        print(f"💵 TOTAL: ${total:.2f}")

    @classmethod
    def checkout(cls):
        cls.show_cart()
        if cls.items:
            confirm = input("Confirm purchase? (y/n): ").lower()
            if confirm == 'y':
                print("💳 Purchase completed! Thank you!")
                cls.items.clear()
                cls.save_to_file()

    @classmethod
    def save_to_file(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'price'])
                for item in cls.items:
                    writer.writerow([item.name, item.price])
        except IOError as e:
            print(f"❌ Error saving cart: {e}")

    @classmethod
    def load_from_file(cls):
        try:
            with open(cls.FILE, 'r') as file:
                reader = csv.DictReader(file)
                cls.items = [
                    Product(row['name'], float(row['price']))
                    for row in reader if row['name'] and row['price']
                ]
        except FileNotFoundError:
            pass
        except (ValueError, KeyError) as e:
            print(f"❌ Error loading cart: {e}")

def main():
    ProductManager.load_from_file()
    Cart.load_from_file()
    
    menu = {
        '1': ('Manage Products', product_menu),
        '2': ('View Cart', Cart.show_cart),
        '3': ('Checkout', Cart.checkout),
        '4': ('Exit', None)
    }

    def product_menu():
        sub_menu = {
            '1': ('Add Product', ProductManager.add_product),
            '2': ('Delete Product', ProductManager.delete_product),
            '3': ('View Products', ProductManager.show_products),
            '4': ('Add to Cart', Cart.add_item),
            '5': ('Remove from Cart', Cart.remove_item),
            '6': ('Back', None)
        }
        
        while True:
            print("\n🛍️  Product Management")
            print("=" * 30)
            for k, (v, _) in sub_menu.items():
                print(f"{k}. {v}")
                
            choice = input("\nEnter choice (1-6): ")
            if choice == '6':
                break
            if choice in sub_menu:
                sub_menu[choice][1]()
            else:
                print("❌ Invalid choice!")

    while True:
        print("\n🛒 Shopping System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-4): ")
        if choice == '4':
            ProductManager.save_to_file()
            Cart.save_to_file()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()