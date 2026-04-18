import pymysql
import pandas as pd
import joblib

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
#         return db

#     except Exception as e:
#         print("Database Connection Error:", e)
#         exit()

from utils.db_connection import get_connection

db = get_connection()


# ===============================
# FETCH DATA
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
# LOAD TRAINED MODEL
# ===============================
def load_model():
    try:
        model = joblib.load("ml_model/isolation_forest_model.pkl")
        print("Model loaded successfully")
        return model

    except Exception as e:
        print("Error loading model:", e)
        exit()


# ===============================
# PREDICT ANOMALIES (FAST)
# ===============================
def detect_anomalies(df, model):
    try:
        preds = model.predict(df[['amount']])

        df['is_fraud'] = [1 if x == -1 else 0 for x in preds]

        fraud_count = df['is_fraud'].sum()
        print(f"Detected {fraud_count} anomalies")

        return df

    except Exception as e:
        print("Prediction Error:", e)
        exit()


# ===============================
# STORE ALERTS (BULK INSERT)
# ===============================
def store_alerts(df):
    try:
        db = get_connection()
        cursor = db.cursor()

        # Filter only fraud rows
        fraud_df = df[df['is_fraud'] == 1]

        if fraud_df.empty:
            print("No fraud detected")
            return

        # Prepare bulk data
        values = [
            (
                int(row['transaction_id']),
                int(row['account_id']),
                "ML Anomaly Detection",
                "HIGH"
            )
            for _, row in fraud_df.iterrows()
        ]

        insert_query = """
        INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
        VALUES (%s, %s, %s, %s)
        """

        cursor.executemany(insert_query, values)

        db.commit()
        cursor.close()
        db.close()

        print(f"{len(values)} ML alerts inserted")

    except Exception as e:
        print("Error storing alerts:", e)
        exit()


# ===============================
# MAIN PIPELINE
# ===============================
def run_ml_detection():
    print("\n--- ML ANOMALY DETECTION (OPTIMIZED) ---")

    df = fetch_transactions()

    if df.empty:
        print("No data found")
        return

    model = load_model()

    df = detect_anomalies(df, model)

    store_alerts(df)

    print("--- PROCESS COMPLETED ---\n")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    run_ml_detection()