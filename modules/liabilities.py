import streamlit as st
import pandas as pd

def liabilities_page():
    st.title("Manage Liabilities")

    # Sub-navigation for direct/indirect liabilities
    liability_type = st.selectbox("Liability Type", ["Direct", "Indirect"])

    with st.form("add_liability"):
        st.subheader(f"Add New {liability_type} Liability")

        lender = st.text_input("Lender/Source")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        duration = st.number_input("Duration (in months)", min_value=0)
        deadline = st.date_input("Deadline")
        remark = st.text_area("Remark")

        if liability_type == "Direct":
            loan_type = st.selectbox("Loan Type", ["Mortgage", "Personal Loan", "Credit Card Debt", "Other"])
            if loan_type == "Mortgage":
                property_value = st.number_input("Property Value", min_value=0.0, step=0.01)
            elif loan_type == "Personal Loan":
                purpose = st.text_input("Purpose of Loan")

        submit = st.form_submit_button("Add Liability")
        if submit:
            new_entry = pd.DataFrame([[liability_type, lender, amount, interest_rate, duration, deadline, remark]],
                                     columns=st.session_state.liabilities_data.columns)
            st.session_state.liabilities_data = pd.concat([st.session_state.liabilities_data, new_entry], ignore_index=True)
            st.success(f"{liability_type} Liability added successfully!")

    # Displaying current liabilities
    st.subheader(f"Current {liability_type} Liabilities")
    st.data_editor(st.session_state.liabilities_data, height=300)
