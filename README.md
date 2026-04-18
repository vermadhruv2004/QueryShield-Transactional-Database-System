# 🔐 QueryShield – Fraud Detection System

A DBMS + Machine Learning based project for detecting fraudulent banking transactions using SQL triggers, stored procedures, and anomaly detection.

---

## 📌 Project Overview

QueryShield is an intelligent banking fraud detection system that:

- Manages customers, accounts, and transactions  
- Detects fraud using DBMS rules (triggers & procedures)  
- Uses Machine Learning (Isolation Forest) for anomaly detection  
- Visualizes fraud insights through a Streamlit dashboard  

---

## 🚀 Features

- Transaction Management (Deposit, Withdrawal, Transfer)  
- Fraud Detection using SQL Triggers  
- Stored Procedures for analysis  
- ML-based Anomaly Detection (Isolation Forest)  
- Real-time Dashboard (Streamlit)  
- Interactive Filters (Date, Account)  
- Fraud Trend Analysis  

---

## 🛠️ Tech Stack

- Database: MySQL  
- Backend: Python  
- ML Model: Scikit-learn (Isolation Forest)  
- Frontend: Streamlit  
- Libraries: pandas, matplotlib, pymysql, joblib  

---

## 📂 Project Structure

queryshield/
│
├── database/
│ ├── schema.sql
│ ├── triggers.sql
│ └── procedures.sql
│
├── data/
│ ├── sample_data.sql
│ └── data_generator.py
│
├── ml_model/
│ ├── anomaly_detection.py
│ └── train_model.py
│
├── dashboard/
│ ├── app.py
│ └── charts.py
│
├── utils/
│ └── db_connection.py
│
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup

1. Clone Repository:
   git clone https://github.com/your-username/queryshield.git
   cd queryshield

2. Install Dependencies:
   pip install -r requirements.txt

3. Setup Database:
   Run schema.sql, triggers.sql, procedures.sql, sample_data.sql

4. Configure DB:
   Update utils/db_connection.py

5. Generate Data:
   python data/data_generator.py

6. Train Model:
   python ml_model/train_model.py

7. Run Detection:
   python ml_model/anomaly_detection.py

8. Run Dashboard:
   streamlit run dashboard/app.py

---

## 📊 Dashboard Features

- Total Transactions & Fraud Count  
- Pie & Bar Charts  
- Fraud Trend Line Chart  
- Filters (Date & Account)  
- ML Detected Frauds  

---

## 🧠 Machine Learning

- Model: Isolation Forest  
- Detects anomalies in transactions  
- Saved using joblib  

---

## 👨‍💻 Author

Dhruv Verma  
Year: 2025  

---

## 📌 Future Enhancements

- Real-time alerts  
- Advanced ML models  
- API integration  

---

## 📜 License

Educational Use Only
