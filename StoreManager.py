from typing import List, Dict

class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} (Stock: {self.stock})"

class Store:
    products: List[Product] = []

    @classmethod
    def add_product(cls):
        try:
            name = input("Product name: ").strip()
            price = float(input("Price: $"))
            stock = int(input("Stock quantity: "))
            if not name or price <= 0 or stock < 0:
                raise ValueError("Invalid input")
            cls.products.append(Product(name, price, stock))
            print("Product added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    @classmethod
    def show_products(cls):
        if not cls.products:
            print("No products available.")
            return
        print("\nProduct List:")
        print("-" * 40)
        for idx, product in enumerate(cls.products, 1):
            print(f"{idx}. {product}")

class Cart:
    items: Dict[Product, int] = {}

    @classmethod
    def add_to_cart(cls):
        Store.show_products()
        if not Store.products:
            return
        try:
            choice = int(input("Select product number: ")) - 1
            if 0 <= choice < len(Store.products):
                product = Store.products[choice]
                quantity = int(input(f"Quantity (max {product.stock}): "))
                if 0 < quantity <= product.stock:
                    cls.items[product] = cls.items.get(product, 0) + quantity
                    product.stock -= quantity
                    print("Added to cart!")
                else:
                    print("Invalid quantity!")
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a valid number!")

    @classmethod
    def show_cart(cls):
        if not cls.items:
            print("Your cart is empty.")
            return
        total = 0.0
        print("\nYour Shopping Cart:")
        print("-" * 40)
        for product, quantity in cls.items.items():
            subtotal = product.price * quantity
            print(f"{product.name} x{quantity} = ${subtotal:.2f}")
            total += subtotal
        print("-" * 40)
        print(f"TOTAL: ${total:.2f}")

def main():
    menu = {
        '1': ('Add Product', Store.add_product),
        '2': ('View Products', Store.show_products),
        '3': ('Add to Cart', Cart.add_to_cart),
        '4': ('View Cart', Cart.show_cart),
        '5': ('Checkout', None),
        '6': ('Exit', None)
    }

    while True:
        print("\nStore Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
        
        choice = input("\nEnter your choice (1-6): ")
        if choice == '5':
            Cart.show_cart()
            print("Thank you for your purchase!")
            Cart.items.clear()
        elif choice == '6':
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()