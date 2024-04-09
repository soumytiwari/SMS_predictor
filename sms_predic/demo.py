import random
import re
import string
import datetime
from faker import Faker

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


acc_no = generate_account_number()
u_email = fake.email()
u_name = fake.name()
date=generate_date()
time=generate_time()
p_no = generate_phone_number()
acc_type = random.choice(['Checking', 'Savings'])
acc_name = random.choice(['Woodgrove Financial', 'Blue Ridge Bank', 'Starlight Credit Union', 'Horizon Trust', 'Sapphire Bank', 'Pinecrest Financial'])

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

print(m_txt)

# Parse message text
account_number_match = re.search(r'Account: \*\*\*\*\*\*\*\*(\d{4})', m_txt)
print('account_number_match: ', account_number_match)
account_type_match = re.search(r'\((\w+) Account\)', m_txt)
print('account_type_match: ', account_type_match)
bank_name_match = re.search(r'Bank: (\w+( \w+)*)', m_txt)
print('bank_name_match: ', bank_name_match)
date_match = re.search(r'Date: (\d{4}-\d{2}-\d{2})', m_txt)
print('date_match: ', date_match)
time_match = re.search(r'Time: (\d{2}:\d{2}:\d{2})', m_txt)
print('time_match: ', time_match)
transaction_id_match = re.search(r'Transaction ID: (TXN\d+)', m_txt)
print('transaction_id_match: ', transaction_id_match)
transaction_type_match = re.search(r'Transaction Type: (\w+ \w+)', m_txt)
print('transaction_type_match: ', transaction_type_match)
transaction_category_match = re.search(r'Transaction Category: (\w+)', m_txt)
print('transaction_category_match: ', transaction_category_match)
amount_match = re.search(r'Amount: \$([\d,]+\.\d+)', m_txt)
print('amount_match: ', amount_match)
from_account_type_match = re.search(r"From: (.*?)'s (\w+) \*\*\*\*\*\*\*\*\d{4}", m_txt)
print('from_account_type_match: ', from_account_type_match)
from_account_number_match = re.search(r"From: \w+( \w+)*'s \w+ \*\*\*\*\*\*\*\*(\d{4})", m_txt)
print('from_account_number_match: ', from_account_number_match)
to_name_match = re.search(r"To: (\w+( \w+)*)'s Savings", m_txt)
print('to_name_match: ', to_name_match)
to_account_number_match = re.search(r"To: \w+( \w+)*'s Savings \*\*\*\*\*\*\*\*(\d{4})", m_txt)
print('to_account_number_match: ', to_account_number_match)
new_checking_balance_match = re.search(r"New (\w+) Balance: \$([\d,]+\.\d+)", m_txt)
print('new_checking_balance_match: ', new_checking_balance_match )
new_savings_balance_match = re.search(r"New Savings Balance: \$([\d,]+\.\d+)", m_txt)
print('new_savings_balance_match: ', new_savings_balance_match)
user_email_match = re.search(r"User Email: (\S+@\S+)", m_txt)
print('user_email_match: ', user_email_match)

if account_number_match and account_type_match and bank_name_match and date_match and time_match and transaction_id_match and transaction_type_match and transaction_category_match and amount_match and from_account_type_match and from_account_number_match and to_name_match and to_account_number_match and new_checking_balance_match and new_savings_balance_match and user_email_match:
    print('Match found!')
    print('Account Number:', account_number_match.group(1))
    print('Account Type:', account_type_match.group(1))
    print('Bank Name:', bank_name_match.group(1))
    print('Date:', date_match.group(1))
    print('Time:', time_match.group(1))
    print('Transaction ID:', transaction_id_match.group(1))
    print('Transaction Type:', transaction_type_match.group(1))
    print('Transaction Category:', transaction_category_match.group(1))
    print('Amount:', amount_match.group(1))
    print('From Account Type:', from_account_type_match.group(2).capitalize())
    print('From Name:', from_account_type_match.group(1))
    print('From Account Number:', from_account_number_match.group(2))
    print('To Name:', to_name_match.group(1))
    print('To Account Number:', to_account_number_match.group(2))
    print('New Checking Balance:', new_checking_balance_match.group(2))
    print('New Savings Balance:', new_savings_balance_match.group(1))
    print('User Email:', user_email_match.group(1))
else:
    print('Match not found.')



# current date and time
# Date: {datetime.date.today().strftime('%m/%d/%Y')}
# Time: {datetime.datetime.now().strftime('%I:%M %p')}