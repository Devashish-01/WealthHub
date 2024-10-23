import streamlit as st
import pandas as pd

def gold_loan_page():
    st.title("Gold Loan")

    with st.form("add_gold_loan", clear_on_submit=True):
        st.subheader("Add Gold Loan")

        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        transaction_date = st.date_input("Transaction Date")
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        weight = st.number_input("Gold Weight (in grams)", min_value=0.0, step=0.01)
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        submit = st.form_submit_button("Add Gold Loan")
        if submit:
            loan_entry = {
                'Loan Type': 'Gold Loan',
                'Bank/Contractor': bank_contractor,
                'Amount': amount,
                'Interest Rate': interest_rate,
                'Interest Type': interest_type,
                'Transaction Date': transaction_date,
                'Duration': duration,
                'Deadline': deadline,
                'Gold Weight': weight,
                'Remark': remark
            }

            new_entry = pd.DataFrame([loan_entry])
            st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
            st.success("Gold Loan added successfully!")

    # Display current gold loans
    st.subheader("Current Gold Loans")
    gold_loans = st.session_state.loans_data[st.session_state.loans_data['Loan Type'] == 'Gold Loan']
    if not gold_loans.empty:
        st.data_editor(gold_loans, height=300)
    else:
        st.info("No gold loans added yet.")
