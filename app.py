import streamlit as st
from modules.dashboard import dashboard_page
from modules.liabilities import liabilities_page
from modules.investments import investments_page
from modules.loans.main_loans import loans_page
from modules.loans.gold_loan import gold_loan_page
from modules.loans.crop_loan import crop_loan_page
from modules.loans.car_loan import car_loan_page
from modules.loans.plot_loan import plot_loan_page
from modules.loans.overdraft import overdraft_page
from modules.summary import summary_page
import pandas as pd

# Initialize session state variables if not already set
if 'liabilities_data' not in st.session_state:
    st.session_state.liabilities_data = pd.DataFrame(columns=[
        'Type', 'Lender', 'Amount', 'Interest Rate', 'Duration', 'Deadline', 'Remark'
    ])

if 'investments_data' not in st.session_state:
    st.session_state.investments_data = pd.DataFrame(columns=[
        'Investment Type', 'Asset', 'Initial Amount', 'Current Value', 'Expected Return', 'Deadline', 'Remark'
    ])

if 'loans_data' not in st.session_state:
    st.session_state.loans_data = pd.DataFrame(columns=[
        'Loan Type', 'Bank/Contractor', 'Amount', 'Interest Rate', 'Interest Type', 'Duration', 'Deadline', 'Remark'
    ])

# Sidebar navigation
st.sidebar.title("Financial Management Tool")
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Liabilities", "Investments", "Loans", "Summary"])

if page == "Dashboard":
    dashboard_page()
elif page == "Liabilities":
    liabilities_page()
elif page == "Investments":
    investments_page()
elif page == "Loans":
    loan_type = st.sidebar.radio("Select Loan Type", ["Main Loans", "Gold Loan", "Crop Loan", "Car Loan", "Plot Loan", "Overdraft"])
    if loan_type == "Main Loans":
        loans_page()
    elif loan_type == "Gold Loan":
        gold_loan_page()
    elif loan_type == "Crop Loan":
        crop_loan_page()
    elif loan_type == "Car Loan":
        car_loan_page()
    elif loan_type == "Plot Loan":
        plot_loan_page()
    elif loan_type == "Overdraft":
        overdraft_page()
elif page == "Summary":
    summary_page()
