import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

# Disable foreign key checks
mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")

table = [
    'user_table', 
    'phone_table', 
    'bank_account', 
    'transaction_table',
    'message_table'
]

# Drop all the tables
for i in table:
    sql = f"DROP TABLE IF EXISTS {i}"
    mycursor.execute(sql)

# sql = 'DROP TABLE IF EXISTS message'
# mycursor.execute(sql)

# Re-enable foreign key checks
mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Commit changes
mydb.commit()

