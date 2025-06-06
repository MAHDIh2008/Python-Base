from typing import List, Dict

class Book:
    def __init__(self, title: str, author: str, copies: int = 1):
        self.title = title
        self.author = author
        self.copies = copies

    def __str__(self):
        return f"'{self.title}' by {self.author} - Copies: {self.copies}"

class Library:
    books: List[Book] = []

    @classmethod
    def _find_book(cls, title: str) -> Book:
        for book in cls.books:
            if book.title.lower() == title.lower():
                return book
        return None

    @classmethod
    def add_book(cls):
        title = input("Title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return
            
        author = input("Author: ").strip()
        if not author:
            print("❌ Author cannot be empty!")
            return
            
        try:
            copies = int(input("Copies: ").strip() or 1)
            if copies <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid copies number!")
            return

        existing = cls._find_book(title)
        if existing:
            existing.copies += copies
            print(f"✅ Added {copies} copies to existing book")
        else:
            cls.books.append(Book(title, author, copies))
            print("✅ New book added successfully!")

    @classmethod
    def borrow_book(cls):
        title = input("Book title: ").strip()
        book = cls._find_book(title)
        if book:
            if book.copies > 0:
                book.copies -= 1
                print(f"✅ Borrowed '{book.title}'. Remaining copies: {book.copies}")
            else:
                print("❌ No copies available!")
        else:
            print("❌ Book not found!")

    @classmethod
    def return_book(cls):
        title = input("Book title: ").strip()
        book = cls._find_book(title)
        if book:
            book.copies += 1
            print(f"✅ Returned '{book.title}'. Total copies now: {book.copies}")
        else:
            print("❌ Book not found in our records!")

    @classmethod
    def show_books(cls):
        if not cls.books:
            print("📚 The library is empty!")
            return
            
        print("\n📚 Library Catalog:")
        print("-" * 60)
        for idx, book in enumerate(cls.books, 1):
            print(f"{idx}. {book}")

def main():
    menu = {
        '1': ('Add Book', Library.add_book),
        '2': ('Borrow Book', Library.borrow_book),
        '3': ('Return Book', Library.return_book),
        '4': ('View Catalog', Library.show_books),
        '5': ('Exit', None)
    }

    while True:
        print("\n📚 Library Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-5): ")
        if choice == '5':
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    # Sample data
    Library.books.append(Book("Python Crash Course", "Eric Matthes", 3))
    Library.books.append(Book("Clean Code", "Robert Martin", 2))
    main()