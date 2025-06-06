from typing import List, Dict

class BankAccount:
    def __init__(self, owner: str, account_number: str):
        self.owner = owner
        self.account_number = account_number
        self.balance: float = 0.0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def __str__(self):
        return f"Account {self.account_number} - Owner: {self.owner} - Balance: ${self.balance:.2f}"

class BankManager:
    accounts: Dict[str, BankAccount] = {}

    @classmethod
    def create_account(cls):
        owner = input("Owner name: ").strip()
        account_number = input("Account number: ").strip()
        if not owner or not account_number:
            print("Owner and account number are required!")
            return
        if account_number in cls.accounts:
            print("Account already exists!")
            return
        cls.accounts[account_number] = BankAccount(owner, account_number)
        print(f"Account created successfully for {owner}")

    @classmethod
    def deposit(cls):
        account_number = input("Account number: ").strip()
        if account_number not in cls.accounts:
            print("Account not found!")
            return
        try:
            amount = float(input("Amount to deposit: $"))
            cls.accounts[account_number].deposit(amount)
            print("Deposit successful!")
        except ValueError as e:
            print(f"Error: {e}")

    @classmethod
    def withdraw(cls):
        account_number = input("Account number: ").strip()
        if account_number not in cls.accounts:
            print("Account not found!")
            return
        try:
            amount = float(input("Amount to withdraw: $"))
            cls.accounts[account_number].withdraw(amount)
            print("Withdrawal successful!")
        except ValueError as e:
            print(f"Error: {e}")

    @classmethod
    def show_accounts(cls):
        if not cls.accounts:
            print("No accounts available.")
            return
        print("\nBank Accounts:")
        print("-" * 60)
        for account in cls.accounts.values():
            print(account)

def main():
    menu = {
        '1': ('Create Account', BankManager.create_account),
        '2': ('Deposit', BankManager.deposit),
        '3': ('Withdraw', BankManager.withdraw),
        '4': ('View All Accounts', BankManager.show_accounts),
        '5': ('Exit', None)
    }

    while True:
        print("\nBank Management System")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
        
        choice = input("\nEnter your choice (1-5): ")
        if choice == '5':
            print("Thank you for using our bank!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()