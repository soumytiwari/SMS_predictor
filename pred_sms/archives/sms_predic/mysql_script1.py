import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# the database was created in mysql_script.py so here already passing it

# ================================================================================================  #

# let's create our tables
mycursor = mydb.cursor()

# USER TABLE
mycursor.execute("CREATE TABLE user_table (u_id INT AUTO_INCREMENT PRIMARY KEY, u_name VARCHAR(255) NOT NULL, u_email VARCHAR(100) NOT NULL, u_add VARCHAR(255) NOT NULL)")
# u_id: 1, 2, 3, ....
# u_name: fake names.. 
# u_email: fake
# u_add: fake
# 50 users
# |
# PHONE NUMBER TABLE
mycursor.execute("CREATE TABLE phone_table (p_id INT AUTO_INCREMENT PRIMARY KEY, p_no VARCHAR(20) NOT NULL, u_id INT, FOREIGN KEY (u_id) REFERENCES user_table(u_id))")
# p_id: 1, 2, 3, ...
# p_no: auto generated
# u_id: 1-1, 2-2, 
# 70 phone numbers.. 1-50: 1-1, 51-70: 1-* (random)

# BANK ACCOUNT TABLE
mycursor.execute("CREATE TABLE bank_account (acc_no VARCHAR(20) PRIMARY KEY, acc_type VARCHAR(50) NOT NULL, acc_balance DECIMAL(10,2) NOT NULL, u_id INT, p_id INT, FOREIGN KEY (u_id) REFERENCES user_table(u_id), FOREIGN KEY (p_id) REFERENCES phone_table(p_id), acc_name VARCHAR(255))")
# acc_no: auto generated
# acc_type: sav/check
# acc_bal: random 10k-50k, .2
# acc_name: bank_name random from array
# u_id: 19-5
# p_id: 19-5
# 100 bank accounts..
# |
# MESSAGE TABLE
mycursor.execute("CREATE TABLE message_table (m_id INT AUTO_INCREMENT PRIMARY KEY, p_id INT, m_txt TEXT NOT NULL, FOREIGN KEY (p_id) REFERENCES phone_table(p_id))")
# 150 bank messages
# m_id: 1, 2, ...
# p_id: 5-5
# m_txt: random texts

# TRANSACTION TABLE
mycursor.execute("CREATE TABLE transaction_table (t_id INT PRIMARY KEY, acc_no VARCHAR(20), acc_type VARCHAR(10), bank_name VARCHAR(200), t_type VARCHAR(120) NOT NULL, t_cat VARCHAR(100) NOT NULL, t_amt INT NOT NULL, t_date DATE NOT NULL, t_time TIME NOT NULL, m_id INT, FOREIGN KEY (m_id) REFERENCES message_table(m_id), FOREIGN KEY (acc_no) REFERENCES bank_account(acc_no))")
# all extracted from the message
# t_id: generated
# acc_no: 5-5
# t_type: online etc.
# t_cat: debit/credit
# t_amt: money
# t_date: date
# t_time: time
# m_id: that-that
# acc_no: that-that
# 150

# TRANSACTION MESSAGE TABLE
mycursor.execute("CREATE TABLE transaction_message (tm_id INT AUTO_INCREMENT PRIMARY KEY, t_id INT, FOREIGN KEY (t_id) REFERENCES transaction_table(t_id), m_id INT, FOREIGN KEY (m_id) REFERENCES message_table(m_id))")
# all extracted from the table
# 150
# tm_id: 1, 2, 3, ...
# t_id: 1-5
# m_id: 1-5

