import streamlit as st
import pandas as pd

def loans_page():
    st.title("Manage Loans")

    with st.form("add_loan", clear_on_submit=True):
        st.subheader("Add New Loan")

        # Select loan type
        loan_type = st.selectbox("Loan Type", ["Gold Loan", "Crop Loan", "Car Loan", "Plot Loan", "Overdraft"])

        # Common fields
        bank_contractor = st.text_input("Bank/Contractor", placeholder="Enter bank or contractor name")
        amount = st.number_input("Loan Amount", min_value=0.0, step=0.01)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.01)
        interest_type = st.selectbox("Interest Type", ["Simple", "Compound"])
        duration = st.number_input("Duration (in months)", min_value=1, step=1)
        deadline = st.date_input("Loan Deadline")
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        # Conditional fields based on loan type
        if loan_type == "Gold Loan":
            weight = st.number_input("Gold Weight (in grams)", min_value=0.0, step=0.01, help="Enter the weight of gold")
        elif loan_type == "Crop Loan":
            crop_type = st.text_input("Type of Crop", placeholder="Enter the type of crop")
        elif loan_type == "Car Loan":
            car_model = st.text_input("Car Model", placeholder="Enter the car model")
            purchase_year = st.number_input("Year of Purchase", min_value=1900, max_value=2100, step=1)
        elif loan_type == "Plot Loan":
            plot_area = st.number_input("Plot Area (in sq ft)", min_value=0.0, step=0.01)
        elif loan_type == "Overdraft":
            overdraft_limit = st.number_input("Overdraft Limit", min_value=0.0, step=0.01)

        # Submit button to add loan entry
        submit = st.form_submit_button("Add Loan")
        if submit:
            try:
                # Prepare the loan entry
                loan_entry = {
                    'Loan Type': loan_type,
                    'Bank/Contractor': bank_contractor,
                    'Amount': amount,
                    'Interest Rate': interest_rate,
                    'Interest Type': interest_type,
                    'Duration': duration,
                    'Deadline': deadline,
                    'Remark': remark
                }

                # Add specific fields based on the loan type
                if loan_type == "Gold Loan":
                    loan_entry['Gold Weight'] = weight
                elif loan_type == "Crop Loan":
                    loan_entry['Crop Type'] = crop_type
                elif loan_type == "Car Loan":
                    loan_entry['Car Model'] = car_model
                    loan_entry['Purchase Year'] = purchase_year
                elif loan_type == "Plot Loan":
                    loan_entry['Plot Area'] = plot_area
                elif loan_type == "Overdraft":
                    loan_entry['Overdraft Limit'] = overdraft_limit

                # Add the entry to the session state
                new_entry = pd.DataFrame([loan_entry])
                st.session_state.loans_data = pd.concat([st.session_state.loans_data, new_entry], ignore_index=True)
                st.success(f"{loan_type} added successfully!")

            except Exception as e:
                st.error(f"An error occurred while adding the loan: {e}")

    # Display current loans
    st.subheader("Current Loans")
    if not st.session_state.loans_data.empty:
        st.data_editor(st.session_state.loans_data, height=300)
    else:
        st.info("No loans added yet.")
