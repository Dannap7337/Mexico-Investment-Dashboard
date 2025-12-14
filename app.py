import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Investment Simulator MX", page_icon="📈")

# Title and Description
st.title("📈 Compound Interest Simulator (Mexico)")
st.markdown("""
This tool visualizes the power of **Compound Interest**. 
Compare keeping your money in cash (0% yield) vs. investing in Mexican Fixed Income instruments 
(like **CETES** or **SOFIPOS**) over time.
""")

# Sidebar for User Inputs
st.sidebar.header("💰 Investment Parameters")

initial_amount = st.sidebar.number_input("Initial Amount ($ MXN)", min_value=1000, value=10000, step=500)
monthly_contribution = st.sidebar.number_input("Monthly Contribution ($)", min_value=0, value=2000, step=100)
years = st.sidebar.slider("Time Horizon (Years)", min_value=1, max_value=10, value=5)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", min_value=1.0, max_value=20.0, value=11.0, help="Avg. rates in Mexico: CETES ~10%, SOFIPOS ~12-14%")

# Calculation Logic
months = years * 12
data = []

invested_balance = initial_amount
cash_balance = initial_amount
total_contributed = initial_amount

for month in range(1, months + 1):
    # Compound Interest Formula (Monthly)
    monthly_yield = invested_balance * ((interest_rate / 100) / 12)
    invested_balance += monthly_yield + monthly_contribution
    
    # Cash Savings (No Yield)
    cash_balance += monthly_contribution
    
    # Total money out of pocket
    total_contributed += monthly_contribution
    
    data.append({
        "Month": month,
        "Invested Balance (Compound Interest)": round(invested_balance, 2),
        "Cash Savings (No Yield)": round(cash_balance, 2),
        "Total Contributed": round(total_contributed, 2)
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# KPI Metrics
col1, col2, col3 = st.columns(3)
total_profit = invested_balance - total_contributed

col1.metric("Final Balance (Invested)", f"${invested_balance:,.2f}")
col2.metric("Balance (Cash Only)", f"${cash_balance:,.2f}")
col3.metric("Net Profit", f"${total_profit:,.2f}", delta_color="normal")

# Chart
st.subheader("Growth Comparison")
st.line_chart(df, x="Month", y=["Invested Balance (Compound Interest)", "Cash Savings (No Yield)"], color=["#00FF00", "#FF0000"])

# Data Table
with st.expander("View detailed monthly breakdown"):
    st.dataframe(df)

st.write("---")
st.caption("Developed by Danna Riveroll | Data Science Engineering Student")