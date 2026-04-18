import random
import pymysql
from datetime import datetime, timedelta

print("Script started...")

# ===============================
# MySQL Connection (with error handling)
# ===============================
# try:
#     db = pymysql.connect(
#     host="localhost",
#     user="queryuser",
#     password="query123",
#     database="queryshield"
# )

#     print("Connected to MySQL")

#     cursor = db.cursor()

# except Exception as e:
#     print("Database Connection Error:", e)
#     exit()

from utils.db_connection import get_connection

db = get_connection()
cursor = db.cursor()

# ===============================
# Helper Data
# ===============================
locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
transaction_types = ["DEPOSIT", "WITHDRAWAL", "TRANSFER"]

# ===============================
# Generate Random Transactions
# ===============================
def generate_transactions(num_records=50):
    try:
        for _ in range(num_records):
            account_id = random.randint(1, 4)
            txn_type = random.choice(transaction_types)

            # Normal vs Fraud Logic
            if random.random() < 0.2:
                amount = random.randint(60000, 150000)
            else:
                amount = random.randint(500, 20000)

            random_time = datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            location = random.choice(locations)

            query = """
            INSERT INTO transactions (account_id, transaction_type, amount, transaction_time, location)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (account_id, txn_type, amount, random_time, location)

            cursor.execute(query, values)

        db.commit()
        print(f"{num_records} transactions inserted successfully!")

    except Exception as e:
        print("Error while inserting data:", e)

# ===============================
# Run Generator
# ===============================
if __name__ == "__main__":
    print("Starting data generation...")
    generate_transactions(100)

    cursor.close()
    db.close()
    print("Connection closed.")