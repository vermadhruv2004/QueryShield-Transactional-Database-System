import pandas as pd
from sklearn.ensemble import IsolationForest
import pymysql
pymysql.install_as_MySQLdb()

# ===============================
# DB CONNECTION
# ===============================
# def get_connection():
#     try:
#         db = pymysql.connect(
#             host="localhost",
#             user="queryuser",
#             password="query123",
#             database="queryshield"
#         )
#         print("Connected to MySQL")
#         return db

#     except Exception as e:
#         print("Database Connection Error:", e)
#         exit()

from utils.db_connection import get_connection

db = get_connection()

# ===============================
# FETCH TRANSACTIONS
# ===============================
def fetch_transactions():
    try:
        db = get_connection()

        query = """
        SELECT transaction_id, account_id, amount
        FROM transactions
        """

        df = pd.read_sql(query, db)
        db.close()

        print(f"Fetched {len(df)} transactions")
        return df

    except Exception as e:
        print("Error fetching data:", e)
        exit()


# ===============================
# ML MODEL (Isolation Forest)
# ===============================
def detect_anomalies(df):
    try:
        model = IsolationForest(contamination=0.1, random_state=42)

        df['anomaly'] = model.fit_predict(df[['amount']])
        df['is_fraud'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

        print("Anomaly detection completed")
        return df

    except Exception as e:
        print("ML Error:", e)
        exit()


# ===============================
# STORE ALERTS
# ===============================
def store_alerts(df):
    try:
        db = get_connection()
        cursor = db.cursor()

        count = 0

        for _, row in df.iterrows():
            if row['is_fraud'] == 1:

                # Prevent duplicate ML alerts
                check_query = """
                SELECT COUNT(*) FROM alerts
                WHERE transaction_id = %s
                AND alert_type = 'ML Anomaly Detection'
                """

                cursor.execute(check_query, (int(row['transaction_id']),))
                result = cursor.fetchone()

                if result[0] == 0:
                    insert_query = """
                    INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
                    VALUES (%s, %s, %s, %s)
                    """

                    values = (
                        int(row['transaction_id']),
                        int(row['account_id']),
                        "ML Anomaly Detection",
                        "HIGH"
                    )

                    cursor.execute(insert_query, values)
                    count += 1

        db.commit()
        cursor.close()
        db.close()

        print(f"{count} ML alerts inserted")

    except Exception as e:
        print("Error storing alerts:", e)
        exit()


# ===============================
# MAIN PIPELINE
# ===============================
def run_ml_detection():
    print("\n--- ML ANOMALY DETECTION STARTED ---")

    df = fetch_transactions()

    if df.empty:
        print("No data found")
        return

    df = detect_anomalies(df)

    store_alerts(df)

    print("--- ML PROCESS COMPLETED ---\n")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    run_ml_detection()