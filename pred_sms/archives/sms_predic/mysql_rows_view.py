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

# for table_name in table:
#     # execute a select query
#     query = f"SELECT * FROM {table_name}"
#     mycursor.execute(query)

#     # fetch all rows
#     rows = mycursor.fetchall()

#     print('TABLE: ', table_name)

#     for row in rows:
#         print(row)

q = "SELECT * FROM user_table"
mycursor.execute(q)
rows = mycursor.fetchall()
i = 0
print('user_table: ')
for row in rows:
    print(row)
    i=i+1
    if i==5:
        break

q = "SELECT * FROM bank_account"
mycursor.execute(q)
rows = mycursor.fetchall()
i = 0
print('phone_table: ')
for row in rows:
    print(row)
    i=i+1
    if i==2:
        break


# close the cursor and connection
mycursor.close()
mydb.close()