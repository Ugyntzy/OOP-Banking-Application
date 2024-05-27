import os  # Importing the os module to facilitate interactions with the operating system.
import random  # Importing the random module to enable the generation of random numbers.
import json  # Importing the json module to handle JSON data manipulation.

# Define the base Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):
        #  Firstly initialize the account attributes with the provided values or defaults
        self.account_number = account_number  # Unique identifier for the each and every account
        self.password = password  #  default password associated with the account for security
        self.account_type = account_type  # Type of the account (e.g., personal, business)
        self.balance = balance  # Initial balance for the account, defaulting to 0.0(zero)

    def deposit(self, amount):
        # Method to add money or deposit to the account balance
        if amount > 0:  #  To ensure the deposit amount is positive
            self.balance += amount  # Increment the balance by the deposit amount (balance + deposit ammount)
            print(f"Deposited ${amount}. New balance is ${self.balance}.")
        else:
            print("Invalid deposit amount. Please enter a positive value.")  # Handle invalid deposit amounts (negative values)

    def withdraw(self, amount):
        # Method to subtract money from the account balance
        if 0 < amount <= self.balance:  # Ensure  that the amount is positive and within the available balance
            self.balance -= amount  # Decrement the balance by the withdrawal amount
            print(f"Withdrew ${amount}. New balance is ${self.balance}.")
        else:
            print("Insufficient funds or invalid amount. Please check your balance and the amount entered.")  # Handle insufficient funds or invalid amounts

    def check_balance(self):
        # Method to display the current account balance
        print(f"Your current balance is ${self.balance}.")

# Define a PersonalAccount class that inherits from the Account class
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize the personal account with the 'personal' account type
        super().__init__(account_number, password, 'personal', balance)

# Define a BusinessAccount class that inherits from the Account class
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize the business account with the 'business' account type
        super().__init__(account_number, password, 'business', balance)

# Define a Bank class to manage multiple accounts and handle account-related operations
class Bank:
    accounts_file = 'accounts.txt'  # Filename where account data will be persistently stored

    def __init__(self):
        self.accounts = self.load_accounts()  # Load existing accounts from the file into the accounts dictionary

    def lzoad_accounts(self):
        # Method to load accounts from the storage file
        if os.path.exists(self.accounts_file):  # Check if the accounts file exists
            with open(self.accounts_file, 'r') as file:  # Open the file in read mode
                return json.load(file)  # Read and parse the JSON data from the file into a dictionary
        return {}  # Return an empty dictionary if the file does not exist

    def save_accounts(self):
        # Method to save the current state of accounts to the storage file
        with open(self.accounts_file, 'w') as file:  # Open the file in write mode
            json.dump(self.accounts, file)  # Convert the accounts dictionary to a JSON string and write it to the file

    def create_account(self, account_type):
        # Method to create a new account based on the specified account type
        account_number = str(random.randint(10000, 99999))  # Generate a random 5-digit account number as a string
        password = str(random.randint(1000, 9999))  # Generate a random 4-digit password as a string
        if account_type == 'personal':
            account = PersonalAccount(account_number, password)  # Create a personal account instance
        elif account_type == 'business':
            account = BusinessAccount(account_number, password)  # Create a business account instance
        else:
            print("Invalid account type. Please enter 'personal' or 'business'.")  # Handle invalid account types
            return None

        # Add the new account details to the accounts dictionary
        self.accounts[account_number] = {
            'password': password,
            'account_type': account_type,
            'balance': account.balance
        }
        self.save_accounts()  # Save the updated accounts dictionary to the file
        print(f"Account created successfully. Account Number: {account_number}, Password: {password}")
        return account

    def login(self, account_number, password):
        # Method to log in to an existing account using the account number and password
        account_data = self.accounts.get(account_number)  # Retrieve the account data from the dictionary
        if account_data and account_data['password'] == password:  # Check if the account exists and the password matches
            if account_data['account_type'] == 'personal':
                return PersonalAccount(account_number, password, account_data['balance'])  # Return a PersonalAccount instance
            elif account_data['account_type'] == 'business':
                return BusinessAccount(account_number, password, account_data['balance'])  # Return a BusinessAccount instance
        print("Invalid account number or password. Please try again.")  # Handle incorrect login details
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        # Method to transfer money from one account to another
        to_account_data = self.accounts.get(to_account_number)  # Retrieve the recipient account data
        if to_account_data:
            if from_account.balance >= amount:  # Ensure there are sufficient funds in the sender's account
                from_account.withdraw(amount)  # Withdraw the specified amount from the sender's account
                self.accounts[from_account.account_number]['balance'] = from_account.balance  # Update the sender's balance in the dictionary
                to_account_data['balance'] += amount  # Increase the recipient's balance by the transfer amount
                self.save_accounts()  # Save the updated account balances to the file
                print(f"Successfully transferred ${amount} to account {to_account_number}.")
            else:
                print("Insufficient funds. Please check your balance.")  # Handle cases where funds are insufficient
        else:
            print("The recipient account does not exist. Please check the account number.")  # Handle non-existing recipient accounts

    def delete_account(self, account_number):
        # Method to delete an existing account
        if account_number in self.accounts:  # Check if the account exists in the dictionary
            del self.accounts[account_number]  # Remove the account from the dictionary
            self.save_accounts()  # Save the updated accounts dictionary to the file
            print(f"Account {account_number} has been deleted successfully.")
        else:
            print("The account does not exist. Please check the account number.")  # Handle non-existing accounts

# Main function to run the banking application and provide a user interface
def main():
    bank = Bank()  # Create an instance of the Bank class

    while True:  # Continuously display the main menu until the user chooses to exit
        print("\nWelcome to the Banking Application")
        print("1. Create Account")  # Option to create a new account
        print("2. Login")  # Option to log in to an existing account
        print("3. Exit")  # Option to exit the application
        choice = input("Choose an option: ")  # Prompt the user to choose an option

        if choice == '1':
            # Handle the option to create a new account
            account_type = input("Enter account type (personal/business): ").strip().lower()  # Prompt for the account type
            bank.create_account(account_type)  # Create the account using the specified type
        elif choice == '2':
            # Handle the option to log in to an existing account
            account_number = input("Enter account number: ").strip()  # Prompt for the account number
            password = input("Enter password: ").strip()  # Prompt for the password
            account = bank.login(account_number, password)  # Attempt to log in with the provided credentials
            if account:
                while True:  # Continuously display the account menu until the user chooses to log out
                    print("\n1. Check Balance")  # Option to check account balance
                    print("2. Deposit Money")  # Option to deposit money into the account
                    print("3. Withdraw Money")  # Option to withdraw money from the account
                    print("4. Transfer Money")  # Option to transfer money to another account
                    print("5. Delete Account")  # Option to delete the account
                    print("6. Logout")  # Option to log out from the account
                    action = input("Choose an option: ")  # Prompt the user to choose an action

                    if action == '1':
                        account.check_balance()  # Display the current account balance
                    elif action == '2':
                        amount = float(input("Enter amount to deposit: "))  # Prompt for the deposit amount
                        account.deposit(amount)  # Deposit the specified amount into the account
                        bank.save_accounts()  # Save the updated account balances to the file
                    elif action == '3':
                        amount = float(input("Enter amount to withdraw: "))  # Prompt for the withdrawal amount
                        account.withdraw(amount)  # Withdraw the specified amount from the account
                        bank.save_accounts()  # Save the updated account balances to the file
                    elif action == '4':
                        to_account_number = input("Enter recipient account number: ").strip()  # Prompt for the recipient's account number
                        amount = float(input("Enter amount to transfer: "))  # Prompt for the transfer amount
                        bank.transfer_money(account, to_account_number, amount)  # Transfer the specified amount to the recipient's account
                    elif action == '5':
                        bank.delete_account(account.account_number)  # Delete the currently logged-in account
                        break  # Exit the account menu after deleting the account
                    elif action == '6':
                        break  # Exit the account menu and log out
                    else:
                        print("Invalid option. Please try again.")  # Handle invalid action choices
        elif choice == '3':
            break  # Exit the main menu and terminate the application
        else:
            print("Invalid option. Please try again.")  # Handle invalid main menu choices

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
