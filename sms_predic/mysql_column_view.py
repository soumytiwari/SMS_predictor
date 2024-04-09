import mysql.connector

# Connect to your MySQL database
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

table = [
    'user_table', 
    'phone_table', 
    'bank_account', 
    'transaction_table', 
    'transaction_message',
    'message_table'
]

print(' ==============================  TABLES  ============================== ')

for table_name in table:
    mycursor.execute(f"SHOW columns FROM {table_name}")
    print('\n', table_name, ": ", [column[0] for column in mycursor.fetchall()])


# close the cursor and connection
mycursor.close()
mydb.close()