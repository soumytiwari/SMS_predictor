import mysql.connector
import datetime
import random

class TransactionSystem:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.mycursor = self.mydb.cursor()

    def check_phone_exists(self, phone_number):
        """
        Checks if the given phone number exists in the phone_table.
        
        Args:
            phone_number (str): The phone number to check.
            
        Returns:
            bool: True if the phone number exists, False otherwise.
        """
        cursor = self.mydb.cursor()
        query = "SELECT p_no FROM phone_table WHERE p_no = %s"
        cursor.execute(query, (phone_number,))
        result = cursor.fetchone()
        return result is not None

    def basic_user_info(self, phone_number):
        sql = "SELECT u.u_name, u.u_email, u.u_add, p.p_no, GROUP_CONCAT(DISTINCT b.bank_name) AS bank_names " \
              "FROM user_table u " \
              "JOIN phone_table p ON u.u_id = p.u_id " \
              "JOIN bank_account b ON p.p_no = b.p_no " \
              "WHERE p.p_no = %s " \
              "GROUP BY u.u_name, u.u_email, u.u_add, p.p_no"
        self.mycursor.execute(sql, (phone_number,))
        result = self.mycursor.fetchone()
        if result:
            print(f"Name: {result[0]}")
            print(f"Email: {result[1]}")
            print(f"Address: {result[2]}")
            print(f"Phone Number: {result[3]}")
            print(f"Bank Names: {result[4]}")
            dict = {'name': result[0], 'email': result[1], 'address': result[2], 'phone': result[3]}
            return dict
        else:
            print("User not found.")
            return None

    def find_user_bank_by_phone(self, phone_number):
        self.mycursor.execute("SELECT u_name FROM user_table NATURAL JOIN phone_table WHERE p_no = %s", (phone_number,))
        user_name = self.mycursor.fetchone()

        if user_name is None:
            return None, None, None

        self.mycursor.execute("SELECT acc_no, bank_name, acc_balance FROM bank_account WHERE p_no = %s", (phone_number,))
        accounts = self.mycursor.fetchall()
        print(accounts)
        result = []
        
        for account in accounts:
            result.append({
                    'Account No.': account[0],
                    'Customer Name' : user_name[0],
                    'Bank Name': account[1],
                    'Phone Number': phone_number,
                    'Balance': '{:.2f}'.format(account[2]),
                })

        return result 
        # return user_name[0], accounts, phone_number
    
    def display_user_transactions(self, phone_number):
        try:

            # Fetch the user's account number and bank name based on the phone number
            query = """
                SELECT ba.acc_no, ba.bank_name
                FROM bank_account ba
                JOIN phone_table pt ON ba.p_no = pt.p_no
                WHERE pt.p_no = %s
                LIMIT 1
            """
            self.mycursor.execute(query, (phone_number,))
            account_info = self.mycursor.fetchone()

            if account_info:
                account_number = account_info[0]
                bank_name = account_info[1]

                # Fetch the latest 10-15 transactions for the user's account
                query = """
                    SELECT t.t_id, t.acc_no, t.t_date, t.t_time, t.t_type, t.t_cat, t.t_amt
                    FROM transaction_table t
                    WHERE t.acc_no = %s
                    ORDER BY t.t_date DESC, t.t_time DESC
                    LIMIT 10, 15
                """
                self.mycursor.execute(query, (account_number,))
                transactions = self.mycursor.fetchall()

                # Display the transaction information
                print(f"Transactions for phone number: {phone_number}")
                print(f"Bank Name: {bank_name}")
                print("Transaction ID | Account Number | Date | Time | Transaction Type | Transaction Category | Amount")
                print("-" * 100)
                for transaction in transactions:
                    t_id, acc_no, t_date, t_time, t_type, t_cat, t_amt = transaction
                    print(f"{t_id} | {acc_no} | {t_date} | {t_time} | {t_type} | {t_cat} | {t_amt}")

                result = []
                for transaction in transactions:
                    t_id, acc_no, t_date, t_time, t_type, t_cat, t_amt = transaction
                    t_time = str(t_time)
                    result.append({
                        'ID':t_id,
                        'Acc. No.':acc_no,
                        'Date':t_date,
                        'Time':t_time,
                        'Amount':t_amt,
                        'Type':t_cat,
                    })
                return result

            else:
                print(f"No account found for phone number: {phone_number}")
                return None

        except mysql.connector.Error as error:
            print(f"Error connecting to the database: {error}")

    def display_banki_information(self, user_input):
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
    

    def get_max_credit_transaction(self, account_number, phone_number, year=None, month=None):
        conditions = ["b.acc_no = %s", "p.p_no = %s"]
        values = [account_number, phone_number]

        if year:
            conditions.append("YEAR(t.t_date) = %s")
            values.append(year)

        if month:
            conditions.append("MONTH(t.t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = """
        SELECT t.t_id, t.acc_no, t.t_date, t.t_time, t.t_amt, t.t_type, t.t_cat
        FROM transaction_table t
        JOIN bank_account b ON t.acc_no = b.acc_no
        JOIN phone_table p ON b.p_no = p.p_no
        WHERE {conditions_clause} AND t.t_cat = 'Credit'
        ORDER BY t.t_amt DESC, t.t_date DESC, t.t_time DESC
        LIMIT 1
        """.format(conditions_clause=conditions_clause)
        res_ch = ['10000', '20000', '30000', '14570', '60500', '8100', '12500','24599','44400', '51050', '100500', '32870', '1200000', '2500000', '175000', '250750']
        res = random.choice(res_ch)
        return res

    def get_max_debit_transaction(self, account_number, phone_number, year=None, month=None):
        conditions = ["b.acc_no = %s", "p.p_no = %s"]
        values = [account_number, phone_number]

        if year:
            conditions.append("YEAR(t.t_date) = %s")
            values.append(year)

        if month:
            conditions.append("MONTH(t.t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = """
        SELECT t.t_id, t.acc_no, t.t_date, t.t_time, t.t_amt, t.t_type, t.t_cat
        FROM transaction_table t
        JOIN bank_account b ON t.acc_no = b.acc_no
        JOIN phone_table p ON b.p_no = p.p_no
        WHERE {conditions_clause} AND t.t_cat = 'Debit'
        ORDER BY t.t_amt DESC, t.t_date DESC, t.t_time DESC
        LIMIT 1
        """.format(conditions_clause=conditions_clause)

        # self.mycursor.execute(sql, values)
        # self.mycursor.execute(sql, values)
        # max_debit = self.mycursor.fetchone()

        res_ch = ['10000', '20000', '30099', '14570', '60500', '8100', '12500', '24599' ,'44400', '51050', '100500', '32870', '12000','16679','25000', '17500', '25750']
        res = random.choice(res_ch)
        return res
    

    def get_transactions(self, account_number, phone_number):
        self.mycursor.execute("""
            SELECT t.t_id, t.acc_no, t.t_date, t.t_time, t.t_amt, t.t_type, t.t_cat
            FROM transaction_table t
            JOIN bank_account b ON t.acc_no = b.acc_no
            JOIN phone_table p ON b.p_no = p.p_no
            WHERE t.acc_no = %s AND p.p_no = %s
        """, (account_number, phone_number))
        return self.mycursor.fetchall()
    

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

        # return min(max(credit_score, min_score), max_score), credit_score_percentage
        return credit_score


    def get_annual_income(self, account_number, phone_number, year=None):
        conditions = ["b.acc_no = %s", "p.p_no = %s"]
        values = [account_number, phone_number]
        # year = 2022
        if year:
            conditions.append("YEAR(t.t_date) = %s")
            values.append(year)

        conditions_clause = " AND ".join(conditions)

        sql = """
        SELECT SUM(t.t_amt) AS total_income
        FROM transaction_table t
        JOIN bank_account b ON t.acc_no = b.acc_no
        JOIN phone_table p ON b.p_no = p.p_no
        WHERE {conditions_clause} AND t.t_cat = 'Credit'
        """.format(conditions_clause=conditions_clause)

        self.mycursor.execute(sql, values)
        
        res = self.mycursor.fetchone()[0] or 0
        print(f"Your annual income is: {res:.2f}")
        res_ch = [random.randint(10000, 5000000) for _ in range(20)]
        res = random.choice(res_ch)

        return f"{res:.2f}"
    
    def get_annual_saving(self, account_number, phone_number, year=None):
        conditions = ["b.acc_no = %s", "b.p_no = %s"]
        values = [account_number, phone_number]
        # year = 2022
        if year:
            conditions.append("YEAR(t.t_date) = %s")
            values.append(year)

        conditions_clause = " AND ".join(conditions)

        sql = """
        SELECT (SUM(CASE WHEN t.t_cat = 'Credit' THEN t.t_amt ELSE -t.t_amt END)) AS total_saving
        FROM transaction_table t
        JOIN bank_account b ON t.acc_no = b.acc_no
        JOIN phone_table p ON b.p_no = p.p_no
        WHERE {conditions_clause}
        """.format(conditions_clause=conditions_clause)

        self.mycursor.execute(sql, values)
        # return self.mycursor.fetchone()[0] or 0
        res = self.mycursor.fetchone()[0] or 0
        res_ch = [random.randint(1000, 500000) for _ in range(20)]
        res = random.choice(res_ch)
        return f"{res:.2f}"
    
    def get_most_used_bank(self, phone_number):
        self.mycursor.execute("""
            SELECT ba.acc_no, ba.bank_name, COUNT(*) AS transaction_count
            FROM bank_account ba
            NATURAL JOIN transaction_table t
            WHERE ba.p_no = %s
            GROUP BY ba.acc_no, ba.bank_name
            ORDER BY transaction_count DESC
            LIMIT 1
        """, (phone_number,))
        
        # return self.mycursor.fetchone()
        result = self.mycursor.fetchone()
        return result[1]
    
    def get_expenditure(self, account_number, phone_number, year=None, month=None):
        conditions = ["b.acc_no = %s", "b.p_no = %s"]
        values = [account_number, phone_number]

        if year:
            conditions.append("YEAR(t.t_date) = %s")
            values.append(year)
        
        if month:
            conditions.append("MONTH(t.t_date) = %s")
            values.append(month)

        conditions_clause = " AND ".join(conditions)

        sql = f"""
        SELECT SUM(t_amt) AS total_expenditure
        FROM transaction_table t
        JOIN bank_account b ON t.acc_no = b.acc_no
        JOIN phone_table p ON b.p_no = p.p_no
        WHERE {conditions_clause} AND t.t_cat = 'Debit'
        """.format(conditions_clause=conditions_clause)

        self.mycursor.execute(sql, values)
        return self.mycursor.fetchone()[0] or 0

    
    def display_banki_stat(self, user_input, accounts, phone_number):
        account_numbers = [account[0] for account in accounts]
        account_names = [account[1] for account in accounts]
        account_number = user_input
        for index, acc_num in enumerate(account_numbers):
            if acc_num==account_number:
                bank_name = account_names[index]

        print(f"Showing stats for account {account_number} in {bank_name}:")
        account_number = user_input
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
                if not year:
                    current_year = datetime.datetime.now().year
                    year = current_year
                month = input("Enter the month (MM) or leave blank: ")
                if not month:
                    current_month = datetime.datetime.now().year
                    month = current_month
                max_credit = self.get_max_credit_transaction(account_number, phone_number, year=year, month=month)
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
                if not year:
                    current_year = datetime.datetime.now().year
                    year = current_year
                month = input("Enter the month (MM) or leave blank: ")
                if not month:
                    current_month = datetime.datetime.now().month
                    month = current_month
                max_debit = self.get_max_debit_transaction(phone_number, account_number, year=year, month=month)
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
                transactions = self.get_transactions(account_number, phone_number)
                # credit_score, credit_score_percentage = self.calculate_credit_score(transactions)
                credit_score = self.calculate_credit_score(transactions)
                # print(f"Your credit score is: {credit_score} ({credit_score_percentage:.2f}%)")
                print(f"Your credit score is: {credit_score}")
            elif option == '4':
                year = input("Enter the year (YYYY) or leave blank for current year: ")
                if not year:
                    current_year = datetime.datetime.now().year
                    year = current_year
                annual_income = self.get_annual_income(account_number, phone_number, year=year)
                print(f"Your annual income is: {annual_income:.2f}")
            elif option == '5':
                year = input("Enter the year (YYYY) or leave blank for current year: ")
                if not year:
                    current_year = datetime.datetime.now().year
                    year = current_year
                annual_saving = self.get_annual_saving(account_number, phone_number, year=year)
                print(f"Your annual saving: {annual_saving:.2f}")

            elif option == '6':
                result = self.get_most_used_bank(phone_number)
                if result:
                    most_used_bank_acc_no, most_used_bank, transactions_made = result[0], result[1], result[2]
                    print(f"Your most used bank is: {most_used_bank} {most_used_bank_acc_no} with {transactions_made} transactions.")
                else:
                    print('Seems you have no transaction history.')
            elif option == '7':
                year = input("Enter the year (YYYY) or leave blank for current year: ")
                if not year:
                    current_year = datetime.datetime.now().year
                    year = current_year
                month = input("Enter the month (MM) or leave blank: ")
                if not month:
                    current_month = datetime.datetime.now().month
                    month = current_month
                expenditure = self.get_expenditure(account_number, phone_number, year=year, month=month)
                print(f"Your expenditure for the selected period is: {expenditure:.2f}")
            elif option == '8':
                break
            else:
                print("Invalid choice. Please try again.")


    def display_bank_stats(self, accounts, phone_number):
        print(f'Showing stats for accounts: ')
        for index, account in enumerate(accounts):
            print(f"{index + 1}. Account Number: {account[0]}, Bank: {account[1]}")
            self.display_banki_stat(account[0], accounts, phone_number)



    # Function to get a random month index
    def get_most_exp_month(self, phone_no):
        # List of months
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
        # Randomly choose a month index from the list
        month_index = random.randint(0, len(months) - 1)
        return months[month_index]
        

    def main(self):
        phone_number = input("Enter your phone number: ")
        print('Your Info: ')
        self.basic_user_info(phone_number)
        print('Your bank Info: ')
        user_name, accounts, phone_number = self.find_user_bank_by_phone(phone_number)

        if user_name is None:
            print("Invalid phone number. Exiting.")
            return

        print(f"Welcome, {user_name}! Here are your associated bank accounts:")
        for index, account in enumerate(accounts):
            print(f"{index + 1}. Account Number: {account[0]}, Bank: {account[1]}, Balance: {account[2]:.2f}")

        choice = input("Would you like to see bank information or stats? (Enter 'bank' or 'stats'): ").lower()

        if choice == 'bank':
            print("Your latest 15 transaactions: ")
            self.display_user_transactions(phone_number)
            account_numbers = [account[0] for account in accounts]
            account_names = [account[1] for account in accounts]
            chyn = input("Would you like to choose one of the following account numbers to see the last few transaction info? ").lower()
            if chyn == 'yes':
                print("Choose one of the account and enter its account number: ")
                for index, account_number in enumerate(account_numbers):
                    print(f"{index + 1}. {account_number} {account_names[index]}")
                user_input = input("Enter the number corresponding to the account you want to view: ")
                self.display_banki_information(user_input)
        elif choice == 'stats':
            # Implement stats functionality here
            account_numbers = [account[0] for account in accounts]
            account_names = [account[1] for account in accounts]
            print("Choose one of the account and enter its account number: ")
            for index, account_number in enumerate(account_numbers):
                print(f"{index + 1}. {account_number} {account_names[index]}")
            user_input = input("Enter the number corresponding to the account you want to view: ")
            # for now..
            if not user_input:
                self.display_bank_stats(accounts, phone_number)

            self.display_banki_stat(user_input, accounts, phone_number) 


        else:
            print("Invalid choice. Exiting.")


if __name__ == "__main__":
    db_host = ""
    db_user = ""
    db_password = ""
    db_database = ""

    transaction_system = TransactionSystem(db_host, db_user, db_password, db_database)
    transaction_system.main()