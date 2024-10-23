import streamlit as st
import pandas as pd

def dashboard_page():
    st.title("Dashboard Overview")

    # Calculate totals
    total_liabilities = st.session_state.liabilities_data['Amount'].sum()
    total_investments = st.session_state.investments_data['Current Value'].sum()
    total_loans = st.session_state.loans_data['Amount'].sum()

    # Calculate monthly interest for liabilities and loans
    monthly_liability_interest = calculate_monthly_liability_interest()
    monthly_loan_interest = calculate_monthly_loan_interest()
    total_monthly_interest = monthly_liability_interest + monthly_loan_interest

    # Calculate outstanding per month
    monthly_outstanding = calculate_monthly_outstanding()

    # Display metrics
    st.metric("Total Liabilities", f"₹{total_liabilities}")
    st.metric("Total Investments", f"₹{total_investments}")
    st.metric("Total Loans", f"₹{total_loans}")
    st.metric("Monthly Interest (Liabilities)", f"₹{monthly_liability_interest:.2f}")
    st.metric("Monthly Interest (Loans)", f"₹{monthly_loan_interest:.2f}")
    st.metric("Total Monthly Interest", f"₹{total_monthly_interest:.2f}")
    st.metric("Monthly Outstanding", f"₹{monthly_outstanding:.2f}")

    # Nearest deadline alert
    nearest_deadline = get_nearest_deadline()
    if nearest_deadline:
        st.warning(f"Nearest Deadline: {nearest_deadline}")

def calculate_monthly_liability_interest():
    # Calculate interest per month for liabilities
    liabilities_data = st.session_state.liabilities_data
    monthly_interest = (liabilities_data['Amount'] * liabilities_data['Interest Rate'] / 12).sum() / 100
    return monthly_interest

def calculate_monthly_loan_interest():
    # Calculate interest per month for loans
    loans_data = st.session_state.loans_data
    monthly_interest = (loans_data['Amount'] * loans_data['Interest Rate'] / 12).sum() / 100
    return monthly_interest

def calculate_monthly_outstanding():
    # Calculate total outstanding amount per month (liabilities + loans)
    liabilities_outstanding = (st.session_state.liabilities_data['Amount'] / st.session_state.liabilities_data['Duration']).sum()
    loans_outstanding = (st.session_state.loans_data['Amount'] / st.session_state.loans_data['Duration']).sum()
    return liabilities_outstanding + loans_outstanding

def get_nearest_deadline():
    # Get the nearest deadline across all data
    deadlines = pd.concat([
        st.session_state.liabilities_data['Deadline'],
        st.session_state.loans_data['Deadline']
    ])
    return deadlines.min() if not deadlines.empty else None
