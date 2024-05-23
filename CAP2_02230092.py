import os  # Importing os module to interact with the operating system.
import random  # Importing random module to generate random numbers.
import json  # Importing json module to work with JSON data.

# Define a base Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):
        # Initialize account attributes
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        # Method to deposit money into the account
        if amount > 0:  # Check if the deposit amount is positive
            self.balance += amount  # Increase the balance by the deposit amount
            print(f"Deposited ${amount}. New balance is ${self.balance}.")
        else:
            print("Invalid deposit amount.")  # Handle invalid deposit amount

    def withdraw(self, amount):
        # Method to withdraw money from the account
        if 0 < amount <= self.balance:  # Check if the amount is positive and within available balance
            self.balance -= amount  # Decrease the balance by the withdrawal amount
            print(f"Withdrew ${amount}. New balance is ${self.balance}.")
        else:
            print("Insufficient funds or invalid amount.")  # Handle insufficient funds or invalid amount

    def check_balance(self):
        # Method to check the current balance
        print(f"Your current balance is ${self.balance}.")

# Define a PersonalAccount class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize with 'personal' account type
        super().__init__(account_number, password, 'personal', balance)

# Define a BusinessAccount class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize with 'business' account type
        super().__init__(account_number, password, 'business', balance)

# Define a Bank class to manage multiple accounts
class Bank:
    accounts_file = 'accounts.txt'  # Filename where account data will be saved

    def __init__(self):
        self.accounts = self.load_accounts()  # Load existing accounts from file

    def load_accounts(self):
        # Method to load accounts from the file
        if os.path.exists(self.accounts_file):  # Check if the file exists
            with open(self.accounts_file, 'r') as file:  # Open the file in read mode
                return json.load(file)  # Load and return the JSON data as a dictionary
        return {}  # Return an empty dictionary if the file does not exist

    def save_accounts(self):
        # Method to save accounts to the file
        with open(self.accounts_file, 'w') as file:  # Open the file in write mode
            json.dump(self.accounts, file)  # Write the accounts dictionary as JSON to the file

    def create_account(self, account_type):
        # Method to create a new account
        account_number = str(random.randint(10000, 99999))  # Generate a random 5-digit account number
        password = str(random.randint(1000, 9999))  # Generate a random 4-digit password
        if account_type == 'personal':
            account = PersonalAccount(account_number, password)  # Create a personal account
        elif account_type == 'business':
            account = BusinessAccount(account_number, password)  # Create a business account
        else:
            print("Invalid account type.")  # Handle invalid account type
            return None

        # Save the new account in the accounts dictionary
        self.accounts[account_number] = {
            'password': password,
            'account_type': account_type,
            'balance': account.balance
        }
        self.save_accounts()  # Save the updated accounts to the file
        print(f"Account created. Account Number: {account_number}, Password: {password}")
        return account

    def login(self, account_number, password):
        # Method to login to an account
        account_data = self.accounts.get(account_number)  # Get account data from the dictionary
        if account_data and account_data['password'] == password:  # Check if account exists and password matches
            if account_data['account_type'] == 'personal':
                return PersonalAccount(account_number, password, account_data['balance'])  # Return personal account object
            elif account_data['account_type'] == 'business':
                return BusinessAccount(account_number, password, account_data['balance'])  # Return business account object
        print("Invalid account number or password.")  # Handle invalid login
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        # Method to transfer money from one account to another
        to_account_data = self.accounts.get(to_account_number)  # Get recipient account data
        if to_account_data:
            if from_account.balance >= amount:  # Check if there are sufficient funds
                from_account.withdraw(amount)  # Withdraw the amount from sender's account
                self.accounts[from_account.account_number]['balance'] = from_account.balance  # Update sender's balance
                to_account_data['balance'] += amount  # Increase recipient's balance
                self.save_accounts()  # Save the updated accounts to the file
                print(f"Transferred ${amount} to account {to_account_number}.")
            else:
                print("Insufficient funds.")  # Handle insufficient funds
        else:
            print("Receiving account does not exist.")  # Handle non-existing recipient account

    def delete_account(self, account_number):
        # Method to delete an account
        if account_number in self.accounts:  # Check if the account exists
            del self.accounts[account_number]  # Delete the account from the dictionary
            self.save_accounts()  # Save the updated accounts to the file
            print(f"Account {account_number} deleted.")
        else:
            print("Account does not exist.")  # Handle non-existing account

# Main function to run the banking application
def main():
    bank = Bank()  # Create a Bank object

    while True:  # Main loop for the banking application
        print("\nWelcome to the Banking Application")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")  # Get user choice

        if choice == '1':
            # Option to create a new account
            account_type = input("Enter account type (personal/business): ").strip().lower()
            bank.create_account(account_type)
        elif choice == '2':
            # Option to login to an existing account
            account_number = input("Enter account number: ").strip()
            password = input("Enter password: ").strip()
            account = bank.login(account_number, password)  # Attempt to login
            if account:
                while True:  # Loop for account actions
                    print("\n1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    action = input("Choose an option: ")  # Get user action choice

                    if action == '1':
                        account.check_balance()  # Check account balance
                    elif action == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)  # Deposit money
                        bank.save_accounts()  # Save changes
                    elif action == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)  # Withdraw money
                        bank.save_accounts()  # Save changes
                    elif action == '4':
                        to_account_number = input("Enter recipient account number: ").strip()
                        amount = float(input("Enter amount to transfer: "))
                        bank.transfer_money(account, to_account_number, amount)  # Transfer money
                    elif action == '5':
                        bank.delete_account(account.account_number)  # Delete account
                        break
                    elif action == '6':
                        break  # Logout
                    else:
                        print("Invalid option. Please try again.")  # Handle invalid action choice
        elif choice == '3':
            break  # Exit the application
        else:
            print("Invalid option. Please try again.")  # Handle invalid main menu choice

if __name__ == "__main__":
    main()  # Run the main function if this script is executed
