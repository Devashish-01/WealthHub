import streamlit as st
import pandas as pd

def crop_loan_page():
    st.title("Crop Loan")

    with st.form("add_crop_loan", clear_on_submit=True):
        st.subheader("Add Crop Loan")

        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        transaction_date = st.date_input("Transaction Date")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        crop_type = st.text_input("Type of Crop", placeholder="Enter the type of crop")
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        submit = st.form_submit_button("Add Crop Loan")
        if submit:
            loan_entry = {
                'Loan Type': 'Crop Loan',
                'Bank/Contractor': bank_contractor,
                'Amount': amount,
                'Interest Rate': interest_rate,
                'Interest Type': interest_type,
                'Transaction Date': transaction_date,
                'Duration': duration,
                'Deadline': deadline,
                'Crop Type': crop_type,
                'Remark': remark
            }

            new_entry = pd.DataFrame([loan_entry])
            st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
            st.success("Crop Loan added successfully!")

    # Display current crop loans
    st.subheader("Current Crop Loans")
    crop_loans = st.session_state.loans_data[st.session_state.loans_data['Loan Type'] == 'Crop Loan']
    if not crop_loans.empty:
        st.data_editor(crop_loans, height=300)
    else:
        st.info("No crop loans added yet.")
