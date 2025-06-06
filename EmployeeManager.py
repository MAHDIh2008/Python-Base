from typing import List, Dict

class Employee:
    _id_counter = 1
    employees: Dict[int, 'Employee'] = {}

    def __init__(self, name: str):
        self.name = name
        self.id = Employee._id_counter
        Employee._id_counter += 1
        Employee.employees[self.id] = self

    def __str__(self):
        return f"ID: {self.id} - Name: {self.name}"

    @classmethod
    def find_by_id(cls, emp_id: int) -> 'Employee':
        return cls.employees.get(emp_id)

    @classmethod
    def find_by_name(cls, name: str) -> List['Employee']:
        return [emp for emp in cls.employees.values() if name.lower() in emp.name.lower()]

    @classmethod
    def show_all(cls):
        if not cls.employees:
            print("👥 No employees registered")
            return
            
        print("\n👥 Employee List:")
        print("-" * 40)
        for emp in sorted(cls.employees.values(), key=lambda x: x.id):
            print(emp)

def main():
    while True:
        print("\n🏢 Employee Management System")
        print("=" * 30)
        print("1. Add Employee")
        print("2. Find by ID")
        print("3. Find by Name")
        print("4. View All Employees")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            name = input("Employee name: ").strip()
            if not name:
                print("❌ Name cannot be empty!")
                continue
            emp = Employee(name)
            print(f"✅ Employee added: {emp}")
            
        elif choice == '2':
            try:
                emp_id = int(input("Employee ID: "))
                emp = Employee.find_by_id(emp_id)
                print(emp if emp else "❌ Employee not found!")
            except ValueError:
                print("❌ Invalid ID format!")
                
        elif choice == '3':
            name = input("Search name: ").strip()
            results = Employee.find_by_name(name)
            if results:
                print("\n🔍 Search Results:")
                print("-" * 40)
                for emp in results:
                    print(emp)
            else:
                print("❌ No matching employees found!")
                
        elif choice == '4':
            Employee.show_all()
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    # Sample data
    Employee("Mahdi")
    Employee("Sara")
    Employee("Ali")
    main()