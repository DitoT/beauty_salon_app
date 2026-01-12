import numpy as np

def total_revenue(df):
    return float(df["price"].sum()) if not df.empty else 0.0

def average_ticket(df):
    return float(np.mean(df["price"])) if not df.empty else 0.0

def revenue_by_service(df):
    return df.groupby("service")["price"].sum()

def revenue_by_employee(df):
    return df.groupby("employee")["price"].sum()
