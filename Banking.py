from datetime import datetime
from functools import wraps
import json

def validate_amount(func):

    @wraps(func)
    def wrapper(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        return func(self, amount)

    return wrapper


def require_login(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        if not self.logged_in:
            raise PermissionError(
                "You must be logged in to perform this action."
            )

        return func(self, *args, **kwargs)

    return wrapper


class Account:

    def __init__(self, account_number, account_holder, balance=0.0,pin=None):
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = balance
        self.transactions = []
        self.logged_in = False
        self.__pin = pin

    @require_login
    @validate_amount
    def deposit(self, amount):

        self.__balance += amount

        self._add_transaction(
            "DEPOSIT",
            amount,
            "Money deposited"
        )

        return self.balance

    def login(self, pin):

        if pin != self.__pin:
            raise ValueError("Incorrect PIN.")

        self.logged_in = True
        print("Login successful.")

    def logout(self):
        self.logged_in = False
        print("Logged out .")

    @require_login
    @validate_amount
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.__balance:
            raise ValueError("Insufficient funds.")

        return self._withdraw(amount)
    

    def _deposit(self, amount):

        self.__balance += amount

        self._add_transaction(
            "TRANSFER",
            amount,
            "Money received"
        )

        return self.balance

    def __str__(self):
        return (
            f"Account Number: {self.account_number}\n"
            f"Holder: {self.account_holder}\n"
            f"Balance: ${self.balance:.2f}"
        )

    def show_transactions(self):
         print("\n".join(self.transactions)) 

    @property
    def balance(self):
        return self.__balance

    def _withdraw(self, amount):

        self.__balance -= amount

        self._add_transaction(
            "WITHDRAW",
            amount,
            "Money withdrawn"
        )

        return self.balance
    def _add_transaction(self, transaction_type, amount, details=""):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        transaction = (
            f"{time} | {transaction_type} | "
            f"₹{amount:.2f} | {details}"
        )

        self.transactions.append(transaction)

    def show_statement(self):

        print("\n" + "=" * 40)
        print("           ACCOUNT STATEMENT")
        print("=" * 40)

        print(f"Account Number : {self.account_number}")
        print(f"Account Holder : {self.account_holder}")
        print(f"Current Balance: ₹{self.balance:.2f}")

        print("\nTransaction History")
        print("-" * 40)

        if not self.transactions:
            print("No transactions found.")
        else:
            for transaction in self.transactions:
                print(transaction)

        print("=" * 40)


class SavingsAccount(Account):

    @require_login
    @validate_amount
    def withdraw(self, amount):

        if self.balance - amount < 500:
            raise ValueError(
                "Withdrawal denied. Minimum balance of ₹500 must be maintained."
            )

        return super().withdraw(amount)

class CurrentAccount(Account):

    OVERDRAFT_LIMIT = 2000

    @require_login
    @validate_amount
    def withdraw(self, amount):

        if amount > self.balance + self.OVERDRAFT_LIMIT:
            raise ValueError(
                "Withdrawal denied. Overdraft limit of ₹2000 exceeded."
            )

        return self._withdraw(amount)
 
class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account):
    
        if account.account_number in self.accounts:
            raise ValueError("Account already exists.")

        self.accounts[account.account_number] = account

        print("Account created successfully.")

    def find_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account not found.")
        return self.accounts[account_number]

    def transfer(self, sender_number, receiver_number, amount):

        sender = self.find_account(sender_number)
        receiver = self.find_account(receiver_number)

        if sender_number == receiver_number:
            raise ValueError("Cannot transfer money to the same account.")

        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")

        if not sender.logged_in:
            raise PermissionError("Sender must be logged in.")

        if amount > sender.balance + getattr(sender, "OVERDRAFT_LIMIT", 0):
            raise ValueError("Insufficient funds for transfer.")

        sender.withdraw(amount)
        receiver._deposit(amount)

        sender._add_transaction(
            "TRANSFER",
            amount,
            f"Transferred to Account {receiver_number}"
        )

        print("Transfer successful.")

    def show_all_accounts(self):

        if not self.accounts:
            print("No accounts found.")
            return

        print("\n" + "=" * 60)
        print("                 ALL ACCOUNTS")
        print("=" * 60)

        for account_number, account in self.accounts.items():

            if isinstance(account, SavingsAccount):
                account_type = "Savings"
            elif isinstance(account, CurrentAccount):
                account_type = "Current"
            else:
                account_type = "Regular"

            print(
                f"Account No: {account_number} | "
                f"Holder: {account.account_holder} | "
                f"Type: {account_type} | "
                f"Balance: ₹{account.balance:.2f}"
            )

        print("=" * 60)

    def save_accounts(self):

        data = {}

        for account_number, account in self.accounts.items():

            if isinstance(account, SavingsAccount):
                account_type = "SavingsAccount"

            elif isinstance(account, CurrentAccount):
                account_type = "CurrentAccount"

            else:
                account_type = "Account"

            data[account_number] = {
                "account_type": account_type,
                "account_number": account.account_number,
                "account_holder": account.account_holder,
                "balance": account.balance,
                "transactions": account.transactions,
                "pin": account._Account__pin
            }

        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Accounts saved successfully.")

    def load_accounts(self):

        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            print("No saved accounts found.")
            return

        for account_number, account_data in data.items():

            account_type = account_data["account_type"]

            if account_type == "SavingsAccount":

                account = SavingsAccount(
                    account_data["account_number"],
                    account_data["account_holder"],
                    account_data["balance"],
                    account_data["pin"]
                )

            elif account_type == "CurrentAccount":

                account = CurrentAccount(
                    account_data["account_number"],
                    account_data["account_holder"],
                    account_data["balance"],
                    account_data["pin"]
                )

            else:

                account = Account(
                    account_data["account_number"],
                    account_data["account_holder"],
                    account_data["balance"],
                    account_data["pin"]
                )

            account.transactions = account_data["transactions"]

            self.accounts[int(account_number)] = account


        print("Accounts loaded successfully.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid amount.")

def create_account_menu(bank):

    print("\n" + "=" * 45)
    print("            CREATE ACCOUNT")
    print("=" * 45)

    try:
        account_number = get_int("Enter account number: ")
        account_holder = input("Enter account holder name: ")
        balance = get_float("Enter initial balance: ")
        pin = int(input("Create PIN: "))

        print("\nChoose Account Type:")
        print("1. Savings Account")
        print("2. Current Account")

        account_type = input("Enter choice: ")

        if account_type == "1":
            account = SavingsAccount(
                account_number,
                account_holder,
                balance,
                pin
            )

        elif account_type == "2":
            account = CurrentAccount(
                account_number,
                account_holder,
                balance,
                pin
            )

        else:
            print("Invalid account type.")
            return

        bank.create_account(account)

    except ValueError as e:
        print("Error:", e)


def login_menu(bank):

    print("\n" + "=" * 45)
    print("                 LOGIN")
    print("=" * 45)

    try:
        account_number = int(input("Enter account number: "))
        pin = int(input("Enter PIN: "))

        account = bank.find_account(account_number)

        account.login(pin)

        account_menu(bank, account)

    except (ValueError, PermissionError) as e:
        print("Error:", e)


def account_menu(bank, account):

    while account.logged_in:

        print("\n" + "=" * 45)
        print(f"           WELCOME, {account.account_holder}")
        print("=" * 45)

        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Account Statement")
        print("7. Logout")

        choice = input("\nEnter your choice: ")

        try:

            if choice == "1":

                print(f"\nCurrent Balance: ₹{account.balance:.2f}")

            elif choice == "2":

                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)

                print(f"Deposit successful.")
                print(f"New Balance: ₹{account.balance:.2f}")

            elif choice == "3":

                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)

                print(f"Withdrawal successful.")
                print(f"New Balance: ₹{account.balance:.2f}")

            elif choice == "4":

                receiver_number = int(
                    input("Enter receiver account number: ")
                )

                amount = float(
                    input("Enter transfer amount: ")
                )

                bank.transfer(
                    account.account_number,
                    receiver_number,
                    amount
                )

                print(f"New Balance: ₹{account.balance:.2f}")

            elif choice == "5":

                account.show_transactions()

            elif choice == "6":

                account.show_statement()

            elif choice == "7":

                account.logout()

            else:

                print("Invalid choice.")

        except (ValueError, PermissionError) as e:

            print("Error:", e)


def find_account_menu(bank):

    print("\n" + "=" * 45)
    print("             FIND ACCOUNT")
    print("=" * 45)

    try:
        account_number = get_int("Enter account number: ")

        account = bank.find_account(account_number)

        print("\nAccount found!")
        print(f"Account Number : {account.account_number}")
        print(f"Account Holder : {account.account_holder}")
        print(f"Balance        : ₹{account.balance:.2f}")

        if isinstance(account, SavingsAccount):
            print("Account Type   : Savings")

        elif isinstance(account, CurrentAccount):
            print("Account Type   : Current")

        else:
            print("Account Type   : Regular")

    except ValueError as e:
        print("Error:", e)



def main_menu(bank):

    while True:

        print("\n" + "=" * 45)
        print("        🏦 BANKING MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Create Account")
        print("2. Login")
        print("3. Show All Accounts")
        print("4. Find Account")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_account_menu(bank)

        elif choice == "2":
            login_menu(bank)

        elif choice == "3":
            bank.show_all_accounts()

        elif choice == "4":
            find_account_menu(bank)

        elif choice == "5":
            bank.save_accounts()
            print("Thank you for using the Banking System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    bank = Bank()
    bank.load_accounts()
    main_menu(bank)


# bank = Bank()

# bank.load_accounts()

# main_menu(bank)

# bank = Bank()

# account1 = SavingsAccount(1001, "Sonu", 5000, 1234)
# account2 = CurrentAccount(1002, "Rahul", 3000, 5678)

# bank.create_account(account1)
# bank.create_account(account2)

# # Login Sonu
# account1.login(1234)

# # Deposit
# account1.deposit(1000)
# print("Sonu balance:", account1.balance)

# # Withdraw
# account1.withdraw(500)
# print("Sonu balance:", account1.balance)

# # Transfer ₹1000 to Rahul
# bank.transfer(1001, 1002, 1000)

# print("\n--- Sonu Statement ---")
# account1.show_statement()

# print("\n--- Rahul Statement ---")
# account2.show_statement()

