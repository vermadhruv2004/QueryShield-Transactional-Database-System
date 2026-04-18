import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db_connection import get_connection

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="QueryShield Dashboard", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>🔐 QueryShield Fraud Detection Dashboard</h1>
""", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data(ttl=5)
def load_data():
    db = get_connection()
    transactions = pd.read_sql("SELECT * FROM transactions", db)
    alerts = pd.read_sql("SELECT * FROM alerts", db)
    db.close()
    return transactions, alerts

transactions, alerts = load_data()

# ===============================
# 🔍 FILTERS
# ===============================
st.sidebar.header("🔍 Filters")

# Date filter
transactions['transaction_time'] = pd.to_datetime(transactions['transaction_time'])

min_date = transactions['transaction_time'].min()
max_date = transactions['transaction_time'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Account filter
account_ids = transactions['account_id'].unique()
selected_account = st.sidebar.selectbox(
    "Select Account",
    ["All"] + list(account_ids)
)

# Apply filters
filtered_txn = transactions.copy()

if len(date_range) == 2:
    filtered_txn = filtered_txn[
        (filtered_txn['transaction_time'] >= pd.to_datetime(date_range[0])) &
        (filtered_txn['transaction_time'] <= pd.to_datetime(date_range[1]))
    ]

if selected_account != "All":
    filtered_txn = filtered_txn[filtered_txn['account_id'] == selected_account]

filtered_alerts = alerts[alerts['transaction_id'].isin(filtered_txn['transaction_id'])]

# ===============================
# 📊 KPI SECTION
# ===============================
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

total_txn = len(filtered_txn)
total_alerts = len(filtered_alerts)
fraud_percent = (total_alerts / total_txn * 100) if total_txn > 0 else 0

col1.metric("💳 Transactions", total_txn)
col2.metric("🚨 Alerts", total_alerts)
col3.metric("⚠️ Fraud %", f"{fraud_percent:.2f}%")

st.divider()

# ===============================
# 📊 CHARTS (HORIZONTAL LAYOUT)
# ===============================
col1, col2 = st.columns(2)

# Pie Chart
with col1:
    st.subheader("Fraud Distribution (Pie)")
    alert_counts = filtered_alerts['alert_type'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(alert_counts, labels=alert_counts.index, autopct='%1.1f%%')
    st.pyplot(fig1)

# Horizontal Bar Chart
with col2:
    st.subheader("Fraud Distribution (Horizontal Bar)")
    fig2, ax2 = plt.subplots()
    alert_counts.sort_values().plot(kind='barh', ax=ax2)
    st.pyplot(fig2)

st.divider()

# ===============================
# 📈 FRAUD TREND (LINE CHART)
# ===============================
st.subheader("📈 Fraud Trend Over Time")

if not filtered_alerts.empty:
    merged = filtered_alerts.merge(
        transactions[['transaction_id', 'transaction_time']],
        on='transaction_id'
    )

    merged['date'] = pd.to_datetime(merged['transaction_time']).dt.date

    trend = merged.groupby('date').size()

    fig3, ax3 = plt.subplots()
    trend.plot(kind='line', marker='o', ax=ax3)
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Fraud Count")

    st.pyplot(fig3)
else:
    st.warning("No fraud data for selected filters")

st.divider()

# ===============================
# 📋 TABLES
# ===============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Transactions")
    st.dataframe(filtered_txn.tail(10), use_container_width=True)

with col2:
    st.subheader("🚨 Alerts")
    st.dataframe(filtered_alerts.tail(10), use_container_width=True)

# ===============================
# 🤖 ML ALERTS
# ===============================
st.subheader("🤖 ML Detected Frauds")

ml_alerts = filtered_alerts[filtered_alerts['alert_type'] == "ML Anomaly Detection"]
st.dataframe(ml_alerts, use_container_width=True)


st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>
        © 2025 Dhruv Verma | QueryShield DBMS Project
    </p>
            
    <style>
    .stApp {
        background-color: #0E1117;
    }
    </style>
""", unsafe_allow_html=True)