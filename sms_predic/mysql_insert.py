import random
import string
import datetime
from faker import Faker
import mysql.connector


mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

# Create a Faker instance for generating fake data
fake = Faker()

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))


def generate_phone_number():
    return ''.join(random.choices(string.digits, k=10))


def generate_date():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=random.randint(365*5, 365*10))
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date


def generate_time():
    random_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    return random_time

def generate_transaction_id(date, time):
    transaction_id = f"TXN{date.strftime('%Y%m%d')}{time.strftime('%H%M%S')}"
    return transaction_id

def generate_transaction_category():
    transaction_category=random.choice(['Debit', 'Credit'])
    return transaction_category

def generate_message_text(user_name, new_name, account_number, account_type, transaction_type, transaction_category, amount, from_account, to_account, new_balance_checking, new_balance_savings, user_email, bank_name, date, time, transaction_id, phone_no):

    date=generate_date()
    time=generate_time()
    txn = generate_transaction_id(date, time)
    transaction_category=generate_transaction_category()
    p_no2=generate_phone_number()

    if (transaction_category=='Credit'):
        t=new_name
        new_name=user_name
        user_name=t
        from_account=generate_account_number()
        to_account=acc_no
        t=phone_no
        phone_no=p_no2
        p_no2=t

    message = f"""Transaction Alert for {user_name}

Account: ********{account_number[-4:]} ({account_type} Account)
Bank: {bank_name}
Date: {date}
Time: {time}
Transaction ID: {transaction_id}
Transaction Type: {transaction_type}
Transaction Category: {transaction_category}

Description: {transaction_type}

Amount: ${amount:.2f}
From: {user_name}'s {account_type} ********{from_account[-4:]} (Phone: +{phone_no})
To: {new_name}'s Savings ********{to_account[-4:]}  (Phone: +{p_no2})

New {account_type} Balance: ${new_balance_checking:.2f}
New Savings Balance: ${new_balance_savings:.2f}

User Email: {user_email}

Thank you for banking with {bank_name}."""
    return message

# Insert data into tables
for _ in range(100):


    # Insert data into user_table (checked!)
    u_name = fake.name()
    u_email = fake.email()
    u_add = fake.address()
    sql = "INSERT INTO user_table (u_name, u_email, u_add) VALUES (%s, %s, %s)"
    val = (u_name, u_email, u_add)
    mycursor.execute(sql, val)
    u_id = mycursor.lastrowid

    # Insert data into phone_table
    p_no = generate_phone_number()
    sql = "INSERT INTO phone_table (p_no, u_id) VALUES (%s, %s)"
    val = (p_no, u_id)
    mycursor.execute(sql, val)
    p_id = mycursor.lastrowid
    

    # Insert data into bank_account
    acc_no = generate_account_number()
    acc_type = random.choice(['Checking', 'Savings', 'Current', 'Salary', 'Fixed Deposit', 'Recurring Deposit', 'NRI'])
    acc_balance = round(random.uniform(1000, 50000), 2)
    acc_name = random.choice(['Woodgrove Financial', 'Blue Ridge Bank', 'Starlight Credit Union', 'Horizon Trust', 'Sapphire Bank', 'Pinecrest Financial'])
    sql = "INSERT INTO bank_account (acc_no, acc_type, acc_balance, u_id, p_id, acc_name) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (acc_no, acc_type, acc_balance, u_id, p_id, acc_name)
    mycursor.execute(sql, val)
    

    # Insert data into message_table
    date=generate_date()
    time=generate_time()
    txn = generate_transaction_id(date, time)

    m_txt = generate_message_text(
            user_name=u_name,
            new_name=fake.name(),
            account_number=acc_no,
            account_type=acc_type,
            transaction_type=random.choice(['Online Transfer', 'ATM Withdrawal', 'Deposit']),
            transaction_category=generate_transaction_category(),
            amount=round(random.uniform(100, 5000), 2),
            from_account=acc_no,
            to_account=generate_account_number(),
            new_balance_checking=round(random.uniform(1000, 50000), 2),
            new_balance_savings=round(random.uniform(1000, 50000), 2),
            user_email=u_email,
            bank_name=acc_name,
            date=date,
            time=time,
            transaction_id=txn,
            phone_no=p_no
        )
    sql = "INSERT INTO message_table (p_id, m_txt) VALUES (%s, %s)"
    val = (p_id, m_txt)
    mycursor.execute(sql, val) 

# Commit the changes to the database
mydb.commit()
