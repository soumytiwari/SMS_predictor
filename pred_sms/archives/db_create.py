import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password=""
)

print(mydb)

# Create a cursor object
mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE trans_database")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)