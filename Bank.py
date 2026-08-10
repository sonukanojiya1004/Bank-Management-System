class BankAccount:
    def __init__(self, account_holder, initial_balance=0.0, account_number=None):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.account_number = account_number or self._generate_account_number()

    @staticmethod
    def _generate_account_number():
        import random
        return str(random.randint(100000, 999999))

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return (
            f"Account Number: {self.account_number}\n"
            f"Holder: {self.account_holder}\n"
            f"Balance: ${self.balance:.2f}"
        )


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_holder, initial_balance=0.0):
        account = BankAccount(account_holder, initial_balance)
        self.accounts[account.account_number] = account
        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def list_accounts(self):
        return list(self.accounts.values())

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if not account:
            raise ValueError("Account not found.")
        return account.deposit(amount)

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if not account:
            raise ValueError("Account not found.")
        return account.withdraw(amount)

    def transfer(self, from_account_number, to_account_number, amount):
        sender = self.get_account(from_account_number)
        receiver = self.get_account(to_account_number)
        if not sender or not receiver:
            raise ValueError("One or both accounts were not found.")
        sender.withdraw(amount)
        receiver.deposit(amount)
        return sender.balance, receiver.balance

    def show_menu(self):
        print("\nBanking Management System")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transfer Money")
        print("6. View All Accounts")
        print("7. Exit")


def main():
    bank = BankingSystem()

    while True:
        bank.show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter account holder name: ").strip()
            while True:
                try:
                    initial_balance = float(input("Enter initial balance: "))
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            account = bank.create_account(name, initial_balance)
            print(f"Account created successfully. Your account number is {account.account_number}")

        elif choice == "2":
            account_number = input("Enter account number: ").strip()
            while True:
                try:
                    amount = float(input("Enter deposit amount: "))
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            try:
                bank.deposit(account_number, amount)
                print("Deposit successful.")
            except ValueError as exc:
                print(exc)

        elif choice == "3":
            account_number = input("Enter account number: ").strip()
            while True:
                try:
                    amount = float(input("Enter withdrawal amount: "))
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            try:
                bank.withdraw(account_number, amount)
                print("Withdrawal successful.")
            except ValueError as exc:
                print(exc)

        elif choice == "4":
            account_number = input("Enter account number: ").strip()
            account = bank.get_account(account_number)
            if account:
                print(f"Current balance: ${account.balance:.2f}")
            else:
                print("Account not found.")

        elif choice == "5":
            from_account = input("Enter sender account number: ").strip()
            to_account = input("Enter receiver account number: ").strip()
            while True:
                try:
                    amount = float(input("Enter transfer amount: "))
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            try:
                bank.transfer(from_account, to_account, amount)
                print("Transfer successful.")
            except ValueError as exc:
                print(exc)

        elif choice == "6":
            accounts = bank.list_accounts()
            if not accounts:
                print("No accounts found.")
            else:
                for account in accounts:
                    print("-" * 25)
                    print(account)

        elif choice == "7":
            print("Thank you for using the Banking Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
