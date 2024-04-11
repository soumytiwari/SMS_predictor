import datetime
import string
import random
from faker import Faker
import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()

fake = Faker()

def generate_unique_account_number():
    sql = "SELECT COUNT(*) FROM bank_account"
    mycursor.execute(sql)
    count = mycursor.fetchone()[0]

    if count == 0: 
        return ''.join(random.choices(string.digits, k=10))
    else:
        while True:
            acc_no = ''.join(random.choices(string.digits, k=10))
            sql = "SELECT acc_no FROM bank_account WHERE acc_no LIKE %s"
            val = (f'%{acc_no[-4:]}',)
            mycursor.execute(sql, val)
            if not mycursor.fetchone():
                return acc_no
            
def generate_unique_phone_number():
    sql = "SELECT COUNT(*) FROM phone_table"
    mycursor.execute(sql)
    count = mycursor.fetchone()[0]

    if count == 0: 
        return ''.join(random.choices(string.digits, k=10))
    else:
        while True:
            p_no = ''.join(random.choices(string.digits, k=10))
            sql = "SELECT p_no FROM phone_table WHERE p_no LIKE %s"
            val = (f'%{p_no[-4:]}',)
            mycursor.execute(sql, val)
            if not mycursor.fetchone():
                return p_no


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

def generate_message_text(user_name, acc_num, acc_type, bank_name, transaction_id, date, time, transaction_type, amount, transaction_category, new_balance, user_email):
    message = f"""Transaction Alert for {user_name}!

Account: ********{acc_num[-4:]} ({acc_type} Account)
Bank: {bank_name}

Transaction Details:
- Transaction ID: {transaction_id}
- Date: {date}
- Time: {time}
- Type: {transaction_type}
- Amount: ${amount:.2f}
- Category: {transaction_category}


Account Balances:
- New Balance: ${new_balance:.2f}

User Email: {user_email}
If you didn't make the transaction, please contact our customer support.
Thank you for banking with {bank_name}.
"""
    return message


user_ids = []
phone_numbers = []
bank_accounts = []

# Generate users
for _ in range(100):
    u_name = fake.name()
    u_email = fake.email()
    u_add = fake.address()
    sql = "INSERT INTO user_table (u_name, u_email, u_add) VALUES (%s, %s, %s)"
    val = (u_name, u_email, u_add)
    mycursor.execute(sql, val)
    u_id = mycursor.lastrowid
    user_ids.append(u_id)

    # Generate at least one phone number for each user
    p_no = generate_unique_phone_number()
    sql = "INSERT INTO phone_table (p_no, u_id) VALUES (%s, %s)"
    val = (p_no, u_id)
    mycursor.execute(sql, val)
    phone_numbers.append(p_no)

    # Generate at least one bank account for each phone number
    acc_no = generate_unique_account_number()
    acc_type = random.choice(['Checking', 'Savings', 'Current', 'Salary', 'Fixed Deposit', 'Recurring Deposit', 'NRI'])
    acc_balance = round(random.uniform(1, 50000000), 2)
    bank_name = random.choice(['Woodgrove Financial', 'Blue Ridge Bank', 'Starlight Credit Union', 'Horizon Trust', 'Sapphire Bank', 'Pinecrest Financial'])
    sql = "INSERT INTO bank_account (acc_no, acc_type, acc_balance, bank_name, p_no) VALUES (%s, %s, %s, %s, %s)"
    val = (acc_no, acc_type, acc_balance, bank_name, p_no)
    mycursor.execute(sql, val)
    bank_accounts.append(acc_no)

# Generate additional phone numbers for random users
for _ in range(50):
    u_id = random.choice(user_ids)
    p_no = generate_unique_phone_number()
    sql = "INSERT INTO phone_table (p_no, u_id) VALUES (%s, %s)"
    val = (p_no, u_id)
    mycursor.execute(sql, val)
    phone_numbers.append(p_no)

# Generate additional bank accounts for random phone numbers
for _ in range(70):
    p_no = random.choice(phone_numbers)
    acc_no = generate_unique_account_number()
    acc_type = random.choice(['Checking', 'Savings', 'Current', 'Salary', 'Fixed Deposit', 'Recurring Deposit', 'NRI'])
    acc_balance = round(random.uniform(1, 50000000), 2)
    bank_name = random.choice(['Woodgrove Financial', 'Blue Ridge Bank', 'Starlight Credit Union', 'Horizon Trust', 'Sapphire Bank', 'Pinecrest Financial'])
    sql = "INSERT INTO bank_account (acc_no, acc_type, acc_balance, bank_name, p_no) VALUES (%s, %s, %s, %s, %s)"
    val = (acc_no, acc_type, acc_balance, bank_name, p_no)
    mycursor.execute(sql, val)
    bank_accounts.append(acc_no)

# Generate transactions and messages
for _ in range(10000):
    acc_no = random.choice(bank_accounts)

    sql = "SELECT p_no FROM bank_account WHERE acc_no = %s"
    mycursor.execute(sql, (acc_no,))
    p_no = mycursor.fetchone()[0]

    sql = "SELECT u_id FROM phone_table WHERE p_no = %s"
    mycursor.execute(sql, (p_no,))
    u_id = mycursor.fetchone()[0]

    sql = "SELECT u_name, u_email FROM user_table WHERE u_id = %s"
    mycursor.execute(sql, (u_id,))
    u_name, u_email = mycursor.fetchone()

    sql = "SELECT acc_type, bank_name FROM bank_account WHERE acc_no = %s"
    mycursor.execute(sql, (acc_no,))
    acc_type, bank_name = mycursor.fetchone()

    date = generate_date()
    time = generate_time()
    txn = generate_transaction_id(date, time)

    transaction_type = random.choice(['Online Transfer', 'ATM Withdrawal', 'Deposit', 'Point of Sale (POS) Purchase', 'Online Purchase', 'Check Deposit', 'Check Payment', 'Direct Deposit', 'Bill Payment', 'Bank Fees', 'Interest Earned', 'Wire Transfer'])
    amount = round(random.uniform(100, 5000), 2)

    if transaction_type in ['Deposit', 'Check Deposit', 'Direct Deposit', 'Interest Earned']:
        transaction_category = 'Credit'
    elif transaction_type in ['ATM Withdrawal', 'Point of Sale (POS) Purchase', 'Online Purchase', 'Check Payment', 'Bill Payment', 'Bank Fees']:
        transaction_category = 'Debit'
    else:
        transaction_category = random.choice(['Debit', 'Credit'])

    new_balance = round(random.uniform(1000, 50000), 2)

    m_txt = generate_message_text(
        user_name=u_name,
        acc_num=acc_no,
        acc_type=acc_type,
        bank_name=bank_name,
        transaction_id=txn,
        date=date,
        time=time,
        transaction_type=transaction_type,
        amount=amount,
        transaction_category=transaction_category,
        new_balance=new_balance,
        user_email=u_email
    )

    sql = "INSERT INTO message_table (m_id, p_no, m_txt) VALUES (NULL, %s, %s)"
    val = (p_no, m_txt)
    mycursor.execute(sql, val)

    sql = "INSERT INTO transaction_table (t_id, acc_no, t_type, t_cat, t_amt, t_date, t_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (txn, acc_no, transaction_type, transaction_category, amount, date, time)
    mycursor.execute(sql, val)

mydb.commit()