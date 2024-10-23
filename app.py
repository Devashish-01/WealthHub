import streamlit as st
import pandas as pd
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
from modules.utils import load_data, save_data  # Import from utils

# Initialize session state variables
if 'liabilities_data' not in st.session_state:
    load_data()


def load_data():
    try:
        st.session_state.liabilities_data = pd.read_csv('liabilities.csv')
    except FileNotFoundError:
        st.session_state.liabilities_data = pd.DataFrame(columns=[
            'Type', 'Lender', 'Amount', 'Interest Rate', 'Duration', 
            'Deadline', 'Transaction Date', 'Remark'
        ])

    try:
        st.session_state.loans_data = pd.read_csv('loans.csv')
    except FileNotFoundError:
        st.session_state.loans_data = pd.DataFrame(columns=[
            'Loan Type', 'Bank/Contractor', 'Amount', 'Interest Rate', 
            'Interest Type', 'Duration', 'Deadline', 'Transaction Date', 'Remark'
        ])

def save_data():
    st.session_state.liabilities_data.to_csv('liabilities.csv', index=False)
    st.session_state.loans_data.to_csv('loans.csv', index=False)

# Initialize session state variables
if 'liabilities_data' not in st.session_state:
    load_data()

# Sidebar navigation
st.sidebar.title("WealthHub")
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

# Save data before exiting
save_data()
