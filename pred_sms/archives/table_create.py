import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# the database was created in db_create.py so here already passing it

# ================================================================================================  #

# let's create our tables
mycursor = mydb.cursor()

# USER TABLE
mycursor.execute("CREATE TABLE user_table (\
                 u_id INT AUTO_INCREMENT PRIMARY KEY, \
                 u_name VARCHAR(255) NOT NULL, \
                 u_email VARCHAR(100) NOT NULL, \
                 u_add VARCHAR(255) NOT NULL)")

# PHONE NUMBER TABLE
mycursor.execute("CREATE TABLE phone_table (\
                 p_no VARCHAR(20) PRIMARY KEY, \
                 u_id INT, \
                 FOREIGN KEY (u_id) REFERENCES user_table(u_id))")

# BANK ACCOUNT TABLE
mycursor.execute("CREATE TABLE bank_account (\
                 acc_no VARCHAR(20) PRIMARY KEY, \
                 acc_type VARCHAR(50) NOT NULL, \
                 acc_balance DECIMAL(10,2) NOT NULL, \
                 bank_name VARCHAR(255), \
                 p_no VARCHAR(20), \
                 FOREIGN KEY (p_no) REFERENCES phone_table(p_no))")

# MESSAGE TABLE
mycursor.execute("CREATE TABLE message_table (\
                 m_id INT AUTO_INCREMENT PRIMARY KEY, \
                 p_no VARCHAR(20), \
                 m_txt TEXT NOT NULL, \
                 FOREIGN KEY (p_no) REFERENCES phone_table(p_no))")

# TRANSACTION TABLE
mycursor.execute("CREATE TABLE transaction_table (\
                 t_id VARCHAR(30) PRIMARY KEY, \
                 acc_no VARCHAR(20), \
                 t_type VARCHAR(120) NOT NULL, \
                 t_cat VARCHAR(100) NOT NULL, \
                 t_amt INT NOT NULL, \
                 t_date DATE NOT NULL, \
                 t_time TIME NOT NULL, \
                 FOREIGN KEY (acc_no) REFERENCES bank_account(acc_no))")

