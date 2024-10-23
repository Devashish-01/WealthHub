import streamlit as st
import pandas as pd

def investments_page():
    st.title("Manage Investments")

    with st.form("add_investment", clear_on_submit=True):
        st.subheader("Add New Investment")
        investment_type = st.selectbox("Investment Type", ["Real Estate", "Stocks", "Gold", "Others"])
        asset = st.text_input("Asset/Property Name")
        initial_amount = st.number_input("Initial Amount", min_value=0.0, step=0.01)
        deadline = st.date_input("Realization Deadline")
        transaction_date = st.date_input("Transaction Date")
        remark = st.text_area("Remark")

        # Handle additional fields based on investment type
        if investment_type == "Stocks":
            volume = st.number_input("Volume (Number of Shares)", min_value=0, step=1)
            current_price = st.number_input("Current Price per Share", min_value=0.0, step=0.01)
            expected_price = st.number_input("Expected Price per Share", min_value=0.0, step=0.01)
            current_value = volume * current_price
            expected_return = volume * (expected_price - current_price)

        # Other investment types...
        submit = st.form_submit_button("Add Investment")
        if submit:
            investment_entry = {
                'Investment Type': investment_type,
                'Asset': asset,
                'Initial Amount': initial_amount,
                'Current Value': current_value,
                'Expected Return': expected_return,
                'Deadline': deadline,
                'Transaction Date': transaction_date,
                'Remark': remark
            }
            new_entry = pd.DataFrame([investment_entry])
            st.session_state.investments_data = pd.concat([st.session_state.investments_data, new_entry], ignore_index=True)
            st.success("Investment added successfully!")
            save_data()

    st.subheader("Current Investments")
    st.data_editor(st.session_state.investments_data, height=300)
