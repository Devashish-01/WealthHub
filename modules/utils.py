import streamlit as st
import pandas as pd

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
