import mysql.connector

class TransactionSystem:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.mycursor = self.mydb.cursor()

    def find_user_by_phone(self, phone_number):
        self.mycursor.execute("SELECT u_name FROM user_table NATURAL JOIN phone_table WHERE p_no = %s", (phone_number,))
        user_name = self.mycursor.fetchone()

        if user_name is None:
            return None, None, None

        self.mycursor.execute("SELECT acc_no, bank_name, acc_balance FROM bank_account WHERE p_no = %s", (phone_number,))
        accounts = self.mycursor.fetchall()

        return user_name[0], accounts, phone_number

    def display_bank_information(self, user_input):
        account_number = None
        bank_name = None

        if user_input:
            account_number = user_input
        else:
            print("Please enter a valid account number.")
            return

        self.mycursor.execute("SELECT acc_no, bank_name FROM bank_account WHERE acc_no = %s", (account_number,))
        bank_info = self.mycursor.fetchone()

        if bank_info is None:
            print("Invalid account number.")
            return

        bank_name = bank_info[1]

        self.mycursor.execute("SELECT t_id, acc_no, t_date, t_time, t_amt, t_type, t_cat FROM transaction_table WHERE acc_no = %s ORDER BY t_date DESC, t_time DESC LIMIT 15", (account_number,))
        transactions = self.mycursor.fetchall()

        print(f"Recent 15 transactions for account {account_number} in {bank_name}:")
        for transaction in transactions:
            print(f"Transaction ID: {transaction[0]}")
            print(f"Account Number: {transaction[1]}")
            print(f"Date: {transaction[2]}")
            print(f"Time: {transaction[3]}")
            print(f"Amount: {transaction[4]:.2f}")
            print(f"Type: {transaction[5]}")
            print(f"Category: {transaction[6]}")
            print("-" * 20)

    def main(self):
        phone_number = input("Enter your phone number: ")
        user_name, accounts, phone_number = self.find_user_by_phone(phone_number)

        if user_name is None:
            print("Invalid phone number. Exiting.")
            return

        print(f"Welcome, {user_name}! Here are your associated bank accounts:")
        for account in accounts:
            print(f"Account Number: {account[0]}, Bank: {account[1]}, Balance: {account[2]:.2f}")

        choice = input("Would you like to see bank information or stats? (Enter 'bank' or 'stats'): ").lower()

        if choice == 'bank':
            account_numbers = [account[0] for account in accounts]
            print("Please choose one of the following account numbers:")
            for index, account_number in enumerate(account_numbers):
                print(f"{index + 1}. {account_number}")
            user_input = input("Enter the number corresponding to the account you want to view: ")
            self.display_bank_information(user_input)
        elif choice == 'stats':
            # Implement stats functionality here
            pass
        else:
            print("Invalid choice. Exiting.")


if __name__ == "__main__":
    db_host = ""
    db_user = ""
    db_password = ""
    db_database = ""

    transaction_system = TransactionSystem(db_host, db_user, db_password, db_database)
    transaction_system.main()