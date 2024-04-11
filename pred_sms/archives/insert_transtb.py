import mysql.connector
import re

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

# Retrieve the messages from the message_table
sql = "SELECT m_txt FROM message_table"
mycursor.execute(sql)
messages = mycursor.fetchall()

# Iterate over each message
for message in messages:
    m_txt = message[0]

    # Extract the required information from the m_txt using regular expressions
    acc_no_match = re.search(r'Account: \*{8}(\d{4})', m_txt)
    t_id_match = re.search(r'Transaction ID: (TXN\d+)', m_txt)
    t_date_match = re.search(r'Date: (\d{4}-\d{2}-\d{2})', m_txt)
    t_time_match = re.search(r'Time: (\d{2}:\d{2}:\d{2})', m_txt)
    t_type_match = re.search(r'Type: (.+)', m_txt)
    t_amt_match = re.search(r'Amount: \$(\d+\.\d{2})', m_txt)
    t_cat_match = re.search(r'Category: (.+)', m_txt)

    if (
        acc_no_match and t_id_match and t_date_match and t_time_match and
        t_type_match and t_amt_match and t_cat_match
    ):
        # Extract the values from the regex matches
        acc_no_last_4 = acc_no_match.group(1)
        t_id = t_id_match.group(1)
        t_date = t_date_match.group(1)
        t_time = t_time_match.group(1)
        t_type = t_type_match.group(1)
        t_amt = float(t_amt_match.group(1))
        t_cat = t_cat_match.group(1)

        # Find the matching account number in the bank_account table
        sql = "SELECT acc_no FROM bank_account WHERE acc_no LIKE %s"
        val = (f'%{acc_no_last_4}',)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if result:
            acc_no = result[0]

            # Insert the transaction into the transaction_table
            sql = "INSERT INTO transaction_table (t_id, acc_no, t_type, t_cat, t_amt, t_date, t_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (t_id, acc_no, t_type, t_cat, t_amt, t_date, t_time)
            mycursor.execute(sql, val)

# Commit the changes to the database
mydb.commit()