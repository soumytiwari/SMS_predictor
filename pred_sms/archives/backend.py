import mysql.connector
from datetime import datetime, timedelta

class Main:
    def __init__(self) -> None:
        self.mydb = mydb = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        self.mycursor = self.mydb.cursor()
        self.user_phone = None
        self.bank_name = None

        self.command_handlers = {
            'TXMS': self.txms,
            'STAT': self.stat,
            'ANIN': self.anin,
            'CDSC': self.cdsc,
            'TXNW': self.txnw,
            'TXNM': self.txnm,
            'TXNY': self.txny,
            'MEXP': self.mexp,
            'TRAY': self.tray,
            'SAPY': self.sapy,
            'EXPM': self.expm,
            'FAVB': self.favb,
            'QUIT': self.quit
        }

    def basic_user_info(self):
        sql = "SELECT u.u_name, u.u_email, u.u_add, p.p_no, GROUP_CONCAT(DISTINCT b.bank_name) AS bank_names " \
              "FROM user_table u " \
              "JOIN phone_table p ON u.u_id = p.u_id " \
              "JOIN bank_account b ON p.p_no = b.p_no " \
              "WHERE p.p_no = %s " \
              "GROUP BY u.u_name, u.u_email, u.u_add, p.p_no"
        self.mycursor.execute(sql, (self.user_phone,))
        result = self.mycursor.fetchone()
        if result:
            print(f"Name: {result[0]}")
            print(f"Email: {result[1]}")
            print(f"Address: {result[2]}")
            print(f"Phone Number: {result[3]}")
            print(f"Bank Names: {result[4]}")
            # dict = {'name': result[0], 'email': result[1], 'address': result[2], 'phone number': result[3]}
            # return dict
        else:
            print("User not found.")
            # return None
    
    # def get_bank_info(self, user_phone):
    #     sql1 = "SELECT u.u_name, p.p_no, GROUP_CONCAT(DISTINCT b.bank_name) AS bank_names " \
    #           "FROM user_table u " \
    #           "JOIN phone_table p ON u.u_id = p.u_id " \
    #           "JOIN bank_account b ON p.p_no = b.p_no " \
    #           "WHERE p.p_no = %s " \
    #           "GROUP BY u.u_name, p.p_no"
    #     self.mycursor.execute(sql1, (user_phone,))
    #     result = self.mycursor.fetchone()
    #     if result:
    #         dict = {'name': result[0], 'bank names': result[1]}
    #         return dict
    #     else:
    #         print("User not found.")
    #         return None


    def basic_bank_info(self):
        sql = "SELECT acc_type, acc_balance " \
              "FROM bank_account " \
              "WHERE bank_name = %s AND p_no = %s"
        self.mycursor.execute(sql, (self.bank_name, self.user_phone))
        results = self.mycursor.fetchall()
        if results:
            for result in results:
                print(f"Account Type: {result[0]}")
                print(f"Account Balance: {result[1]}")
        else:
            print("Bank account not found.")

    def menu(self):
        menu = """
==================================== MENU ====================================

Description:
Press the following sequence of numbers mentioned for the respective query

TXMS - See your latest transaction message
STAT - See your stats and features
ANIN - Check your annual income
CDSC - Check your credit score
TXNW - Check your transactions of any week
TXNM - Check your transactions of any month
TXNY - Check your transactions of any year
MEXP - Check your maximum ACCESSED data
TRAY - Check your yearly transaction
SAPY - Check your savings per year
EXPM - Check your expensive months
FAVB - Check your most used bank
QUIT - To Quit
"""
        print(menu)
        print("\nMenu Sent", 'success')

    def handle_cmds(self, cmd: str) -> str:
        try:
            self.cmd = cmd[:4]
        except:
            self.cmd = None
        return cmd

    def op_impl(self):
        while True:
            try:
                cmd = input("\nEnter your desired query >> ").upper()
                cmd = self.handle_cmds(cmd)
                if cmd:
                    if cmd in self.command_handlers:
                        self.command_handlers[cmd]()
                    else:
                        print('\nInvalid command! Please enter a valid command.')
            except KeyboardInterrupt:
                print('\nKey Board interrupted, closing connection..')
                break

    def txms(self):
            sql = "SELECT m_txt FROM message_table WHERE p_no = %s ORDER BY m_id DESC LIMIT 1"
            self.mycursor.execute(sql, (self.user_phone,))
            result = self.mycursor.fetchone()
            if result:
                print(f"Latest Transaction Message: {result[0]}")
            else:
                print("No transaction message found.")

    def stat(self):
        self.basic_user_info()
        self.basic_bank_info()

    def txnw(self):
        start_date = input("Enter the start date of the week (YYYY-MM-DD): ")
        end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)
        end_date = end_date.strftime("%Y-%m-%d")

        sql = "SELECT * FROM transaction_table WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) AND t_date BETWEEN %s AND %s"
        self.mycursor.execute(sql, (self.user_phone, start_date, end_date))
        results = self.mycursor.fetchall()
        if results:
            print("Transactions for the week:")
            for row in results:
                print(f"Transaction ID: {row[0]}, Type: {row[2]}, Category: {row[3]}, Amount: {row[4]}, Date: {row[5]}, Time: {row[6]}")
        else:
            print("No transactions found for the specified week.")

    def txnm(self):
        month = input("Enter the month (MM): ")
        year = input("Enter the year (YYYY): ")

        sql = "SELECT * FROM transaction_table WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) AND DATE_FORMAT(t_date, '%m-%Y') = %s-%s"
        self.mycursor.execute(sql, (self.user_phone, month, year))
        results = self.mycursor.fetchall()
        if results:
            print(f"Transactions for {month}/{year}:")
            for row in results:
                print(f"Transaction ID: {row[0]}, Type: {row[2]}, Category: {row[3]}, Amount: {row[4]}, Date: {row[5]}, Time: {row[6]}")
        else:
            print(f"No transactions found for {month}/{year}.")

    def txny(self):
        year = input("Enter the year (YYYY): ")

        sql = "SELECT * FROM transaction_table WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) AND DATE_FORMAT(t_date, '%Y') = %s"
        self.mycursor.execute(sql, (self.user_phone, year))
        results = self.mycursor.fetchall()
        if results:
            print(f"Transactions for {year}:")
            for row in results:
                print(f"Transaction ID: {row[0]}, Type: {row[2]}, Category: {row[3]}, Amount: {row[4]}, Date: {row[5]}, Time: {row[6]}")
        else:
            print(f"No transactions found for {year}.")

    def mexp(self):
        sql = "SELECT t_cat, MAX(t_amt) AS max_exp FROM transaction_table WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) GROUP BY t_cat ORDER BY max_exp DESC LIMIT 1"
        self.mycursor.execute(sql, (self.user_phone,))
        result = self.mycursor.fetchone()
        if result:
            print(f"Maximum SAVING/EXPENDITURE Category: {result[0]}")
            print(f"Maximum SAVING/EXPENDITURE Amount: {result[1]}")
        else:
            print("No transaction data found.")

    def tray(self):
        year = input("Enter the year (YYYY): ")

        sql = "SELECT DATE_FORMAT(t_date, '%Y') AS year, SUM(t_amt) AS total_expenditure " \
              "FROM transaction_table " \
              "WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) " \
              "AND DATE_FORMAT(t_date, '%Y') = %s " \
              "GROUP BY year"
        self.mycursor.execute(sql, (self.user_phone, year))
        result = self.mycursor.fetchone()
        if result:
            print(f"Total transaction amount for {result[0]}: {result[1]}")
        else:
            print(f"No transaction data found for the year {year}.")

    def sapy(self):
        year = input("Enter the year (YYYY): ")

        sql = "SELECT DATE_FORMAT(t_date, '%Y') AS year, SUM(t_amt) AS total_savings " \
              "FROM transaction_table " \
              "WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) " \
              "AND t_type = 'Deposit' " \
              "AND DATE_FORMAT(t_date, '%Y') = %s " \
              "GROUP BY year"
        self.mycursor.execute(sql, (self.user_phone, year))
        result = self.mycursor.fetchone()
        if result:
            print(f"Total Savings for {result[0]}: {result[1]}")
        else:
            print(f"No savings data found for the year {year}.")

    def expm(self):
        sql = "SELECT DATE_FORMAT(t_date, '%M') AS month, SUM(t_amt) AS total_expenditure " \
              "FROM transaction_table " \
              "WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) " \
              "GROUP BY month " \
              "ORDER BY total_expenditure DESC " \
              "LIMIT 1"
        self.mycursor.execute(sql, (self.user_phone,))
        result = self.mycursor.fetchone()
        if result:
            print(f"Most Expensive Month: {result[0]}")
            print(f"Total Expenditure: {result[1]}")
        else:
            print("No transaction data found.")

    def favb(self):
        sql = "SELECT bank_name, COUNT(*) AS transaction_count " \
              "FROM transaction_table t " \
              "JOIN bank_account b ON t.acc_no = b.acc_no " \
              "WHERE b.p_no = %s " \
              "GROUP BY bank_name " \
              "ORDER BY transaction_count DESC " \
              "LIMIT 1"
        self.mycursor.execute(sql, (self.user_phone,))
        result = self.mycursor.fetchone()
        if result:
            print(f"Most Used Bank: {result[0]}")
            print(f"Total Transactions: {result[1]}")
        else:
            print("No transaction data found.")

    def anin(self):
        sql = "SELECT SUM(t_amt) AS annual_income " \
              "FROM transaction_table " \
              "WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s) " \
              "AND t_type = 'Deposit' " \
              "AND DATE_FORMAT(t_date, '%Y') = %s"
        year = input("Enter the year (YYYY): ")
        self.mycursor.execute(sql, (self.user_phone, year))
        result = self.mycursor.fetchone()
        if result:
            print(f"Your annual income for {year} is: {result[0]}")
        else:
            print(f"No income data found for the year {year}.")

    def cdsc(self):
        # Calculate the credit score based on the transaction history
        sql = "SELECT t_type, t_amt, t_date " \
              "FROM transaction_table " \
              "WHERE acc_no IN (SELECT acc_no FROM bank_account WHERE p_no = %s)"
        self.mycursor.execute(sql, (self.user_phone,))
        results = self.mycursor.fetchall()

        credit_score = 700  # Start with a default credit score of 700
        for row in results:
            t_type = row[0]
            t_amt = row[1]
            t_date = row[2]

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
            today = datetime.now().date()
            days_since_transaction = (today - t_date).days
            if days_since_transaction < 30:
                credit_score -= 5
            elif days_since_transaction < 90:
                credit_score -= 3
            elif days_since_transaction < 180:
                credit_score += 3
            else:
                credit_score += 5

        print(f"Your calculated credit score is: {credit_score}")

    def quit(self):
        print('\n221 Goodbye. Exiting...')
        self.mydb.close()
        exit()

if __name__ == "__main__":
    user_input_num = input("\nEnter your mobile number connected to your account whose query you want to know >> ")
    obj = Main()
    obj.user_phone = user_input_num
    obj.basic_user_info()
    user_input_bank = input("\nEnter your bank name whose query you want associated >> ")
    obj.bank_name = user_input_bank
    obj.basic_bank_info()
    obj.menu()
    obj.op_impl()


