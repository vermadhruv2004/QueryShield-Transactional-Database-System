import matplotlib.pyplot as plt

# ===============================
# PIE CHART
# ===============================
def fraud_pie_chart(alerts):
    alert_counts = alerts['alert_type'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        alert_counts,
        labels=alert_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title("Fraud Distribution (Pie Chart)")
    return fig


# ===============================
# BAR CHART (VERTICAL)
# ===============================
def fraud_bar_chart(alerts):
    alert_counts = alerts['alert_type'].value_counts()

    fig, ax = plt.subplots()
    alert_counts.plot(kind='bar', ax=ax)
    ax.set_title("Fraud Distribution (Bar Chart)")
    ax.set_xlabel("Alert Type")
    ax.set_ylabel("Count")
    return fig


# ===============================
# BAR CHART (HORIZONTAL 🔥)
# ===============================
def fraud_bar_chart_horizontal(alerts):
    alert_counts = alerts['alert_type'].value_counts()

    fig, ax = plt.subplots()
    alert_counts.plot(kind='barh', ax=ax)
    ax.set_title("Fraud Distribution (Horizontal Bar)")
    ax.set_xlabel("Count")
    ax.set_ylabel("Alert Type")
    return fig