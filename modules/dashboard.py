import streamlit as st
import pandas as pd

def dashboard_page():
    st.title("Dashboard Overview")

    # Calculate totals
    total_liabilities = st.session_state.liabilities_data['Amount'].sum()
    total_investments = st.session_state.investments_data['Current Value'].sum()
    total_loans = st.session_state.loans_data['Amount'].sum()

    # Calculate monthly interest
    monthly_interest = calculate_monthly_interest()

    # Calculate outstanding per month
    monthly_outstanding = calculate_monthly_outstanding()

    # Display metrics
    st.metric("Total Liabilities", f"₹{total_liabilities}")
    st.metric("Total Investments", f"₹{total_investments}")
    st.metric("Total Loans", f"₹{total_loans}")
    st.metric("Monthly Interest", f"₹{monthly_interest}")
    st.metric("Monthly Outstanding", f"₹{monthly_outstanding}")

    # Nearest deadline alert
    nearest_deadline = get_nearest_deadline()
    if nearest_deadline:
        st.warning(f"Nearest Deadline: {nearest_deadline}")

def calculate_monthly_interest():
    # Calculate interest per month for liabilities and loans
    liabilities_interest = (st.session_state.liabilities_data['Amount'] * st.session_state.liabilities_data['Interest Rate'] / 12).sum() / 100
    loans_interest = (st.session_state.loans_data['Amount'] * st.session_state.loans_data['Interest Rate'] / 12).sum() / 100
    return liabilities_interest + loans_interest

def calculate_monthly_outstanding():
    # Calculate total outstanding per month (liabilities + loans)
    total_duration = (st.session_state.liabilities_data['Duration'].sum() + st.session_state.loans_data['Duration'].sum())
    return (st.session_state.liabilities_data['Amount'].sum() + st.session_state.loans_data['Amount'].sum()) / max(1, total_duration)

def get_nearest_deadline():
    deadlines = pd.concat([
        st.session_state.liabilities_data['Deadline'],
        st.session_state.loans_data['Deadline']
    ])
    return deadlines.min() if not deadlines.empty else None
