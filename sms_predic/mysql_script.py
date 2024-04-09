import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

print(mydb)

# Create a cursor object
mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE mydatabase")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)