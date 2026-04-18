import pymysql
import pandas as pd
from sklearn.ensemble import IsolationForest
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
#         print("Connected to MySQL")
#         return db

#     except Exception as e:
#         print("Database Connection Error:", e)
#         exit()

from utils.db_connection import get_connection

# ===============================
# FETCH DATA
# ===============================
def fetch_data():
    try:
        db = get_connection()

        query = """
        SELECT transaction_id, account_id, amount
        FROM transactions
        """

        df = pd.read_sql(query, db)
        db.close()

        print(f"Fetched {len(df)} records for training")
        return df

    except Exception as e:
        print("Error fetching data:", e)
        exit()


# ===============================
# TRAIN MODEL
# ===============================
def train_model(df):
    try:
        model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )

        model.fit(df[['amount']])

        print("Model trained successfully")
        return model

    except Exception as e:
        print("Training Error:", e)
        exit()


# ===============================
# SAVE MODEL
# ===============================
def save_model(model):
    try:
        joblib.dump(model, "ml_model/isolation_forest_model.pkl")
        print("Model saved as isolation_forest_model.pkl")

    except Exception as e:
        print("Error saving model:", e)


# ===============================
# MAIN
# ===============================
def run_training():
    print("\n--- MODEL TRAINING STARTED ---")

    df = fetch_data()

    if df.empty:
        print("No data available for training")
        return

    model = train_model(df)

    save_model(model)

    print("--- MODEL TRAINING COMPLETED ---\n")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    run_training()