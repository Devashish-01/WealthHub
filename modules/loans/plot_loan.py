import streamlit as st
import pandas as pd

def plot_loan_page():
    st.title("Plot Loan")

    with st.form("add_plot_loan", clear_on_submit=True):
        st.subheader("Add Plot Loan")

        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        plot_area = st.number_input("Plot Area (in sq ft)", min_value=0.0, step=0.01)
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        submit = st.form_submit_button("Add Plot Loan")
        if submit:
            loan_entry = {
                'Loan Type': 'Plot Loan',
                'Bank/Contractor': bank_contractor,
                'Amount': amount,
                'Interest Rate': interest_rate,
                'Interest Type': interest_type,
                'Duration': duration,
                'Deadline': deadline,
                'Plot Area': plot_area,
                'Remark': remark
            }

            new_entry = pd.DataFrame([loan_entry])
            st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
            st.success("Plot Loan added successfully!")

    # Display current plot loans
    st.subheader("Current Plot Loans")
    plot_loans = st.session_state.loans_data[st.session_state.loans_data['Loan Type'] == 'Plot Loan']
    if not plot_loans.empty:
        st.data_editor(plot_loans, height=300)
    else:
        st.info("No plot loans added yet.")
