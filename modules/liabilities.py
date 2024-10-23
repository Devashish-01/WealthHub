import streamlit as st
import pandas as pd
from modules.utils import save_data  # Import the function

def liabilities_page():
    st.title("Manage Liabilities")

    with st.form("add_liability", clear_on_submit=True):
        st.subheader("Add New Liability")
        type_ = st.selectbox("Liability Type", ["Direct", "Indirect"])
        lender = st.text_input("Lender/Source")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Deadline")
        transaction_date = st.date_input("Transaction Date")
        remark = st.text_area("Remark")

        submit = st.form_submit_button("Add Liability")
        if submit:
            new_entry = pd.DataFrame([[type_, lender, amount, interest_rate, duration, deadline, transaction_date, remark]],
                                     columns=st.session_state.liabilities_data.columns)
            st.session_state.liabilities_data = pd.concat([st.session_state.liabilities_data, new_entry], ignore_index=True)
            st.success("Liability added successfully!")
            save_data()  # Now it should work

    st.subheader("Current Liabilities")
    st.data_editor(st.session_state.liabilities_data, height=300)
