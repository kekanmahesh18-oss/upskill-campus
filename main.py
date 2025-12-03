import json
from datetime import datetime


class InsufficientFundsError(Exception):
    """Raised when a withdrawal or transfer exceeds the available balance."""
    pass


class AccountNotFoundError(Exception):
    """Raised when an account number does not exist in the bank database."""
    pass


class Account:
    """Represents a customer's bank account."""

    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.transactions = []  # List of transaction history tuples

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Deposited ₹{amount}")
        )

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Withdrew ₹{amount}")
        )

    def get_balance(self):
        """Return current account balance."""
        return self.balance

    def get_transaction_history(self):
        """Return formatted transaction history."""
        return self.transactions

    def __repr__(self):
        return f"<Account {self.account_number}: {self.name}, Balance: ₹{self.balance:.2f}>"


class Bank:
    """Main Bank class handling all operations."""

    def __init__(self, name):
        self.name = name
        self.accounts = {}  # Dictionary for storing accounts: {acc_no: Account object}

    def create_account(self, account_number, name, initial_deposit=0.0):
        """Create a new bank account."""
        if account_number in self.accounts:
            raise ValueError("Account number already exists.")
        self.accounts[account_number] = Account(account_number, name, initial_deposit)
        print(f"Account created successfully for {name} (A/C No: {account_number})")

    def get_account(self, account_number):
        """Fetch account by number or raise exception."""
        if account_number not in self.accounts:
            raise AccountNotFoundError("Account not found.")
        return self.accounts[account_number]

    def deposit_to_account(self, account_number, amount):
        """Deposit funds into an account."""
        acc = self.get_account(account_number)
        acc.deposit(amount)
        print(f" ₹{amount} deposited to A/C {account_number}")

    def withdraw_from_account(self, account_number, amount):
        """Withdraw funds from an account."""
        acc = self.get_account(account_number)
        acc.withdraw(amount)
        print(f" ₹{amount} withdrawn from A/C {account_number}")

    def transfer(self, from_acc_no, to_acc_no, amount):
        """Transfer funds between accounts."""
        if from_acc_no == to_acc_no:
            raise ValueError("Cannot transfer to the same account.")
        from_acc = self.get_account(from_acc_no)
        to_acc = self.get_account(to_acc_no)
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        print(f"₹{amount} transferred from A/C {from_acc_no} to A/C {to_acc_no}")

    def view_account(self, account_number):
        """Display account details and balance."""
        acc = self.get_account(account_number)
        print(f"\n Account Holder: {acc.name}")
        print(f" Account Number: {acc.account_number}")
        print(f" Balance: ₹{acc.balance:.2f}")
        print("\n Transaction History:")
        for t in acc.get_transaction_history():
            print(f"  {t[0]} - {t[1]}")
        print("-" * 40)

    def save_data(self, filename="bank_data.json"):
        """Save all accounts to file (JSON)."""
        data = {
            acc_no: {
                "name": acc.name,
                "balance": acc.balance,
                "transactions": acc.transactions,
            }
            for acc_no, acc in self.accounts.items()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(" Bank data saved successfully.")

    def load_data(self, filename="bank_data.json"):
        """Load account data from file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for acc_no, info in data.items():
                acc = Account(acc_no, info["name"], info["balance"])
                acc.transactions = info["transactions"]
                self.accounts[acc_no] = acc
            print(" Bank data loaded successfully.")
        except FileNotFoundError:
            print(" No previous data found. Starting fresh.")


def main():
    bank = Bank("AI National Bank")
    bank.load_data()

    while True:
        print("\n==== Welcome to AI National Bank ====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Account Details")
        print("6. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                acc_no = input("Enter new account number: ")
                name = input("Enter account holder name: ")
                deposit = float(input("Initial deposit: "))
                bank.create_account(acc_no, name, deposit)
            elif choice == "2":
                acc_no = input("Enter account number: ")
                amount = float(input("Enter amount: "))
                bank.deposit_to_account(acc_no, amount)
            elif choice == "3":
                acc_no = input("Enter account number: ")
                amount = float(input("Enter amount: "))
                bank.withdraw_from_account(acc_no, amount)
            elif choice == "4":
                from_acc = input("From Account: ")
                to_acc = input("To Account: ")
                amount = float(input("Amount: "))
                bank.transfer(from_acc, to_acc, amount)
            elif choice == "5":
                acc_no = input("Enter account number: ")
                bank.view_account(acc_no)
            elif choice == "6":
                bank.save_data()
                print(" Thank you for banking with us!")
                break
            else:
                print(" Invalid choice. Please try again.")
        except Exception as e:
            print(f" Error: {e}")


if __name__ == "__main__":
    main()
