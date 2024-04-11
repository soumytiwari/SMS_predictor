import random
import re
from datetime import datetime
import mysql.connector


mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

def parse(m_txt):
    account_number_match = re.search(r'Account: \*\*\*\*\*\*\*\*(\d{4})', m_txt)
    account_type_match = re.search(r'\((\w+) Account\)', m_txt)
    bank_name_match = re.search(r'Bank: (\w+( \w+)*)', m_txt)
    date_match = re.search(r'Date: (\d{4}-\d{2}-\d{2})', m_txt)
    time_match = re.search(r'Time: (\d{2}:\d{2}:\d{2})', m_txt)
    transaction_id_match = re.search(r'Transaction ID: (TXN\d+)', m_txt)
    transaction_type_match = re.search(r'Transaction Type: (\w+ \w+)', m_txt)
    transaction_category_match = re.search(r'Transaction Category: (\w+)', m_txt)
    amount_match = re.search(r'Amount: \$([\d,]+\.\d+)', m_txt)
    from_account_type_match = re.search(r"From: (.*?)'s (\w+) \*\*\*\*\*\*\*\*\d{4}", m_txt)
    from_account_number_match = re.search(r"From: \w+( \w+)*'s \w+ \*\*\*\*\*\*\*\*(\d{4})", m_txt)
    to_name_match = re.search(r"To: (\w+( \w+)*)'s Savings", m_txt)
    to_account_number_match = re.search(r"To: \w+( \w+)*'s Savings \*\*\*\*\*\*\*\*(\d{4})", m_txt)
    new_checking_balance_match = re.search(r"New (\w+) Balance: \$([\d,]+\.\d+)", m_txt)
    new_savings_balance_match = re.search(r"New Savings Balance: \$([\d,]+\.\d+)", m_txt)
    user_email_match = re.search(r"User Email: (\S+@\S+)", m_txt)

    match = re.search(r'Account: \*\*\*\*\*\*\*\*(\d{4}) \((\w+) Account\).*?Bank: (\w+( \w+)*).*?Date: (\d{4}-\d{2}-\d{2}).*?Time: (\d{2}:\d{2}:\d{2}).*?Transaction ID: (TXN\d+).*?Transaction Type: (\w+ \w+).*?Transaction Category: (\w+).*?Amount: \$([\d,]+\.\d+).*?From: (.*?)\'s (\w+) \*\*\*\*\*\*\*\*(\d{4}).*?To: (\w+( \w+)*)\'s Savings \*\*\*\*\*\*\*\*(\d{4}).*?New (\w+) Balance: \$([\d,]+\.\d+).*?New Savings Balance: \$([\d,]+\.\d+).*?User Email: (\S+@\S+)', m_txt, re.DOTALL)
    return match

# Retrieve data from message_table
sql = "SELECT m_id, m_txt FROM message_table"
mycursor.execute(sql)
messages = mycursor.fetchall()
i=0

# Parse messages and insert into transaction_table and transaction_message
for m_id, m_txt in messages:
    print(m_txt)
    print(m_id)
    # Parse message text
    match = parse(m_txt)
    # match = re.search(r'Account: \*\*\*\*\*\*\*(\d{4}) \((\w+) Account\).*?Transaction ID: (TXN\d+).*?Transaction Type: (\w+).*?Transaction Category: (\w+).*?Amount: \$([\d,.]+).*?From: My \w+ \*\*\*\*\*\*\*(\d{4}).*?To: John\'s Savings \*\*\*\*\*\*\*(\d{4}).*?New \w+ Balance: \$([\d,.]+).*?New Savings Balance: \$([\d,.]+)', m_txt, re.DOTALL)
    print('match: ', match)
    i=i+1
    if i==5:
        break

    if match:
        acc_no = int(match.group(1))
        t_type = match.group(4)
        t_cat = match.group(5)
        t_amt = float(match.group(6).replace(',', ''))
        from_acc = int(match.group(6))
        to_acc = int(match.group(7))
        new_balance_checking = float(match.group(8).replace(',', ''))
        new_balance_savings = float(match.group(9).replace(',', ''))
        t_date = datetime.now().date()
        t_time = datetime.now().time()

        # Insert into transaction_table
        t_id = random.randint(1000000000, 9999999999)

        # sql = "INSERT INTO transaction_table (t_id, acc_no, t_type, t_cat, t_amt, t_date, t_time, m_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        # val = (t_id, acc_no, t_type, t_cat, t_amt, t_date, t_time, m_id)
        # mycursor.execute(sql, val)

        # # Insert into transaction_message
        # sql = "INSERT INTO transaction_message (t_id, m_id) VALUES (%s, %s)"
        # val = (t_id, m_id)
        # mycursor.execute(sql, val)

# mydb.commit()


