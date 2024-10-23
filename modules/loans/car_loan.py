import streamlit as st
import pandas as pd

def car_loan_page():
    st.title("Car Loan")

    with st.form("add_car_loan", clear_on_submit=True):
        st.subheader("Add Car Loan")

        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        transaction_date = st.date_input("Transaction Date")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        car_model = st.text_input("Car Model", placeholder="Enter the car model")
        purchase_year = st.number_input("Year of Purchase", min_value=1900, max_value=2100, step=1)
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        submit = st.form_submit_button("Add Car Loan")
        if submit:
            loan_entry = {
                'Loan Type': 'Car Loan',
                'Bank/Contractor': bank_contractor,
                'Amount': amount,
                'Interest Rate': interest_rate,
                'Interest Type': interest_type,
                'Transaction Date': transaction_date,
                'Duration': duration,
                'Deadline': deadline,
                'Car Model': car_model,
                'Purchase Year': purchase_year,
                'Remark': remark
            }

            new_entry = pd.DataFrame([loan_entry])
            st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
            st.success("Car Loan added successfully!")

    # Display current car loans
    st.subheader("Current Car Loans")
    car_loans = st.session_state.loans_data[st.session_state.loans_data['Loan Type'] == 'Car Loan']
    if not car_loans.empty:
        st.data_editor(car_loans, height=300)
    else:
        st.info("No car loans added yet.")
