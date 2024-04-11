import mysql.connector
import random
import datetime



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
    
    def calculate_credit_score(self, transactions):
        # Calculate the credit score based on the transaction history
        credit_score = 700  # Start with a default credit score of 700

        for transaction in transactions:
            t_type = transaction[5]
            t_amt = transaction[4]
            t_date = transaction[2]

            # Adjust the credit score based on the transaction type and amount
            if t_type == 'Withdrawal':
                if t_amt > 1000:
                    credit_score -= 50
                elif t_amt > 500:
                    credit_score -= 30
                else:
                    credit_score -= 10
            elif t_type == 'Deposit':
                if t_amt > 1000:
                    credit_score += 20
                elif t_amt > 500:
                    credit_score += 10
                else:
                    credit_score += 5

            # Adjust the credit score based on the transaction date
            today = datetime.date.today()
            days_since_transaction = (today - t_date).days
            if days_since_transaction < 30:
                credit_score -= 5
            elif days_since_transaction < 90:
                credit_score -= 3
            elif days_since_transaction < 180:
                credit_score += 3
            else:
                credit_score += 5

        max_score = 850
        min_score = 300
        credit_score_percentage = (credit_score - min_score) / (max_score - min_score) * 100

        return min(max(credit_score, min_score), max_score), credit_score_percentage


    def get_max_credit_transaction(self, account_number, year=None, month=None):
        conditions = [f"acc_no = '{account_number}'"]
        values = []

        if year:
            conditions.append("YEAR(t_date) = %s")
            values.append(year)

        if month:
            conditions.append("MONTH(t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT t_id, acc_no, t_date, t_time, t_amt, t_type, t_cat
        FROM transaction_table
        WHERE {conditions_clause} AND t_cat = 'Credit'
        ORDER BY t_amt DESC, t_date DESC, t_time DESC
        LIMIT 1
        """
        self.mycursor.execute(sql, values)
        return self.mycursor.fetchone()

    def get_max_debit_transaction(self, account_number, year=None, month=None):
        conditions = [f"acc_no = '{account_number}'"]
        values = []

        if year:
            conditions.append("YEAR(t_date) = %s")
            values.append(year)

        if month:
            conditions.append("MONTH(t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT t_id, acc_no, t_date, t_time, t_amt, t_type, t_cat
        FROM transaction_table
        WHERE {conditions_clause} AND t_cat = 'Debit'
        ORDER BY t_amt DESC, t_date DESC, t_time DESC
        LIMIT 1
        """
        self.mycursor.execute(sql, values)
        return self.mycursor.fetchone()

    def get_annual_income(self, account_number, year=None):
        conditions = [f"acc_no = '{account_number}'"]
        values = []

        if year:
            conditions.append("YEAR(t_date) = %s")
            values.append(year)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT SUM(t_amt) AS total_income
        FROM transaction_table
        WHERE {conditions_clause} AND t_cat = 'Credit'
        """
        self.mycursor.execute(sql, values)
        return self.mycursor.fetchone()[0] or 0

    def get_annual_saving(self, account_number, year=None):
        conditions = [f"acc_no = '{account_number}'"]
        values = []

        if year:
            conditions.append("YEAR(t_date) = %s")
            values.append(year)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT (SUM(CASE WHEN t_cat = 'Credit' THEN t_amt ELSE -t_amt END)) AS total_saving
        FROM transaction_table
        WHERE {conditions_clause}
        """
        self.mycursor.execute(sql, values)
        return self.mycursor.fetchone()[0] or 0

    def get_most_used_bank(self, phone_number):
        self.mycursor.execute("SELECT bank_name, COUNT(*) AS transaction_count FROM bank_account NATURAL JOIN transaction_table WHERE p_no = %s GROUP BY bank_name ORDER BY transaction_count DESC LIMIT 1", (phone_number,))
        return self.mycursor.fetchone()

    def get_expenditure(self, account_number, year=None, month=None):
        conditions = [f"acc_no = '{account_number}'"]
        values = []

        if year:
            conditions.append("YEAR(t_date) = %s")
            values.append(year)

        if month:
            conditions.append("MONTH(t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT SUM(t_amt) AS total_expenditure
        FROM transaction_table
        WHERE {conditions_clause} AND t_cat = 'Debit'
        """
        self.mycursor.execute(sql, values)

        return self.mycursor.fetchone()[0] or 0

    def display_stats(self, user_input, accounts):
        if not user_input:
            print("No account selected. Exiting.")
            return

        account_number = user_input[0]
        bank_name = user_input[1]

        print(f"Showing stats for account {account_number} in {bank_name}:")

        print("\nMax. Amount Credited at Once:")
        max_credit = self.get_max_credit_transaction(account_number)
        if max_credit:
            print(f"Transaction ID: {max_credit[0]}")
            print(f"Date: {max_credit[2]}")
            print(f"Time: {max_credit[3]}")
            print(f"Amount: {max_credit[4]:.2f}")
            print(f"Type: {max_credit[5]}")
            print(f"Category: {max_credit[6]}")

        print("\nMax. Amount Debited at Once:")
        max_debit = self.get_max_debit_transaction(account_number)
        if max_debit:
            print(f"Transaction ID: {max_debit[0]}")
            print(f"Date: {max_debit[2]}")
            print(f"Time: {max_debit[3]}")
            print(f"Amount: {max_debit[4]:.2f}")
            print(f"Type: {max_debit[5]}")
            print(f"Category: {max_debit[6]}")

        print("\nCredit Score:")
        transactions = self.get_transactions(account_number)
        credit_score = self.calculate_credit_score(transactions)
        print(f"Your credit score is: {credit_score}")

        print("\nAnnual Income:")
        annual_income = self.get_annual_income(account_number)
        print(f"Your annual income is: {annual_income:.2f}")

        print("\nAnnual Saving:")
        annual_saving = self.get_annual_saving(account_number)
        print(f"Your annual saving is: {annual_saving:.2f}")

        print("\nMost Used Bank:")
        most_used_bank = self.get_most_used_bank(phone_number)[0]
        print(f"Your most used bank is: {most_used_bank}")

        print("\nExpenditure:")
        expenditure = self.get_expenditure(account_number)
        print(f"Your expenditure for the selected period is: {expenditure:.2f}")

    def get_transactions(self, account_number):
        self.mycursor.execute("SELECT t_id, acc_no, t_date, t_time, t_amt, t_type, t_cat FROM transaction_table WHERE acc_no = %s", (account_number,))
        return self.mycursor.fetchall()


    def main(self):
        phone_number = input("Enter your phone number: ")
        user_name, accounts, phone_number = self.find_user_by_phone(phone_number)

        if user_name is None:
            print("Invalid phone number. Exiting.")
            return

        print(f"Welcome, {user_name}! Here are your associated bank accounts:")
        for index, account in enumerate(accounts):
            print(f"{index + 1}. ******{account[0][-4:]} ({account[1]}) - Balance: {account[2]:.2f}")

        choice = input("Would you like to see bank information or stats? (Enter 'bank' or 'stats'): ").lower()

        if choice == 'bank':
            account_numbers = [account[0] for account in accounts]
            print("Please choose one of the following account numbers:")
            for index, account_number in enumerate(account_numbers):
                print(f"{index + 1}. {account_number}*****")
            user_input = input("Enter the number corresponding to the account you want to view: ")
            self.display_bank_information(user_input)
        elif choice == 'stats':
            print("Please choose one of your bank accounts:")
            for index, account in enumerate(accounts):
                print(f"{index + 1}. {account[1]} - {account[0]}*****")
            user_input = input("Enter the number corresponding to the account you want to view stats for: ")

            if not user_input:
                print("No account selected. Exiting.")
                return

            account_number = accounts[user_input - 1][0]
            bank_name = accounts[user_input - 1][1]

            print(f"Showing stats for account {account_number} in {bank_name}:")

            # Display stats options
            while True:
                print("\nStats Menu:")
                print("1. Max. Amount Credited at Once")
                print("2. Max. Amount Debited at Once")
                print("3. Credit Score")
                print("4. Annual Income")
                print("5. Annual Saving")
                print("6. Most Used Bank")
                print("7. Expenditure")
                print("8. Exit")

                option = input("Enter your choice: ")

                if option == '1':
                    year = input("Enter the year (YYYY) or leave blank for current year: ")
                    month = input("Enter the month (MM) or leave blank: ")
                    max_credit = self.get_max_credit_transaction(account_number, year=year, month=month)
                    if max_credit:
                        print(f"Transaction ID: {max_credit[0]}")
                        print(f"Date: {max_credit[2]}")
                        print(f"Time: {max_credit[3]}")
                        print(f"Amount: {max_credit[4]:.2f}")
                        print(f"Type: {max_credit[5]}")
                        print(f"Category: {max_credit[6]}")
                    else:
                        print("No credit transactions found.")
                elif option == '2':
                    year = input("Enter the year (YYYY) or leave blank for current year: ")
                    month = input("Enter the month (MM) or leave blank: ")
                    max_debit = self.get_max_debit_transaction(account_number, year=year, month=month)
                    if max_debit:
                        print(f"Transaction ID: {max_debit[0]}")
                        print(f"Date: {max_debit[2]}")
                        print(f"Time: {max_debit[3]}")
                        print(f"Amount: {max_debit[4]:.2f}")
                        print(f"Type: {max_debit[5]}")
                        print(f"Category: {max_debit[6]}")
                    else:
                        print("No debit transactions found.")
                elif option == '3':
                    print("\nCredit Score:")
                    transactions = self.get_transactions(account_number)
                    credit_score, credit_score_percentage = self.calculate_credit_score(transactions)
                    print(f"Your credit score is: {credit_score} ({credit_score_percentage:.2f}%)")
                elif option == '4':
                    year = input("Enter the year (YYYY) or leave blank for current year: ")
                    annual_income = self.get_annual_income(account_number, year=year)
                    print(f"Your annual income is: {annual_income:.2f}")
                elif option == '5':
                    year = input("Enter the year (YYYY) or leave blank for current year: ")
                    annual_saving = self.get_annual_saving(account_number, year=year)
                    print(f"Your annual saving: {annual_saving:.2f}")

                elif option == '6':
                    most_used_bank = self.get_most_used_bank(self.user_phone)[0]
                    print(f"Your most used bank is: {most_used_bank}")
                elif option == '7':
                    year = input("Enter the year (YYYY) or leave blank for current year: ")
                    month = input("Enter the month (MM) or leave blank: ")
                    expenditure = self.get_expenditure(account_number, year=year, month=month)
                    print(f"Your expenditure for the selected period is: {expenditure:.2f}")
                elif option == '8':
                    break
                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    db_host = ""
    db_user = ""
    db_password = ""
    db_database = ""

    transaction_system = TransactionSystem(db_host, db_user, db_password, db_database)
    transaction_system.main()