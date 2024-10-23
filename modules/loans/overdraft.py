import streamlit as st
import pandas as pd

def overdraft_page():
    st.title("Overdraft")

    with st.form("add_overdraft", clear_on_submit=True):
        st.subheader("Add Overdraft")

        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        transaction_date = st.date_input("Transaction Date")
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        overdraft_limit = st.number_input("Overdraft Limit", min_value=0.0, step=0.01)
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        submit = st.form_submit_button("Add Overdraft")
        if submit:
            loan_entry = {
                'Loan Type': 'Overdraft',
                'Bank/Contractor': bank_contractor,
                'Amount': amount,
                'Interest Rate': interest_rate,
                'Interest Type': interest_type,
                'Transaction Date': transaction_date,
                'Duration': duration,
                'Deadline': deadline,
                'Overdraft Limit': overdraft_limit,
                'Remark': remark
            }

            new_entry = pd.DataFrame([loan_entry])
            st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
            st.success("Overdraft added successfully!")

    # Display current overdrafts
    st.subheader("Current Overdrafts")
    overdrafts = st.session_state.loans_data[st.session_state.loans_data['Loan Type'] == 'Overdraft']
    if not overdrafts.empty:
        st.data_editor(overdrafts, height=300)
    else:
        st.info("No overdrafts added yet.")
