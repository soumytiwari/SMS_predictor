import datetime
import random

def generate_date():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=random.randint(365*5, 365*10))
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date


def generate_time():
    random_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    return random_time

date=generate_date()
time=generate_time()

def generate_transaction_id(date, time):
    transaction_id = f"TXN{date.strftime('%Y%m%d')}{time.strftime('%H%M%S')}"
    return transaction_id

txn = generate_transaction_id(date, time)
print(txn)