import streamlit as st
import json
import os
from datetime import datetime, timedelta, date , time
from utils import *  # Assuming external functions are implemented correctly

st.title("Repayment Window")
st.header("Provide Details")

DATA_FILE = "liabilities_data.json"

# Load existing data or initialize empty
def load_data(file_path):
    """
    Function to load liability data from a JSON file.
    If the file doesn't exist or is corrupted, return an empty structure.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.warning("Data file is corrupted. Resetting to default structure.")
            return {"liabilities": {}}
    else:
        return {"liabilities": {}}

# Save updated data back to the file
def save_data(data, file_path):
    """
    Save the liabilities data back to the JSON file.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")

liabilities = load_data(DATA_FILE)
liabilities_data = liabilities["liabilities"]

# Step 1: Enter lender name
name = st.text_input("Enter lender name")
if name:
    if name not in liabilities_data:
        st.error("Invalid lender name. Please try again.")
    else:
        # Step 2: Enter loan ID
        loan_id = st.text_input("Enter the loan ID")
        if loan_id:
            if loan_id not in liabilities_data[name]["loans"]:
                st.error("Invalid loan ID for the given lender.")
            else:
                # Step 3: Enter amount
                amount = st.number_input("Enter the repayment amount")
                if amount:
                    # Step 4: Enter remark
                    if amount <= 0:
                        st.error("Amount cannot be 0 or less")
                    else:
                        remark = st.text_input("Enter a remark (optional)")

                        # Checkbox confirmation to proceed with the repayment
                        confirm_repayment = st.checkbox("I confirm this repayment is correct")

                        if st.button("Confirm Repayment") and confirm_repayment:
                            loan = liabilities_data[name]["loans"][loan_id]
                            date_of_repayment = date.today()

                            # Ensure 'previous_emi_date' function is implemented in utils
                            emi = loan["upcoming_emi_list"]
                            previous_emi_date_val = previous_emi_date(emi)
                            next_emi_date = previous_emi_date_val + timedelta(days=30*loan["interest_payment_interval_months"])

                            # Calculate date difference
                            date_diff = (date_of_repayment - previous_emi_date_val).days

                            # Calculate interest made on the repayment amount
                            interest_made = (amount * loan["interest_rate"] * date_diff) / (30 * 100)
                            interest_future = (loan["current_principle"] - amount) * loan["interest_rate"] * loan["interest_payment_interval_months"] / 100

                            if loan["current_principle"] < amount:
                                st.error("Amount is greater than the remaining loan amount.")
                            else:
                                # Proceed with repayment since confirmation checkbox is checked
                                next_id = get_next_id(loan["repayment_list"])
                                loan["current_principle"] -= amount

                                # Prepare repayment object
                                loan["repayment_list"][next_id] = {
                                    "loan_id": loan_id,
                                    "amount": amount,
                                    "date_of_repayment": date_of_repayment.isoformat(),
                                    "time_of_repayment" : str(datetime.datetime.now()),
                                    "remark": remark,
                                    "previous_emi_date": previous_emi_date_val.isoformat(),
                                    "next_emi_date" : next_emi_date.isoformat()
                                }

                                # Handle full repayment
                                if loan["current_principle"] == 0:
                                    loan["active"] = False
                                    emi = remove_further_emi(emi)
                                else:
                                    emi = change_emi_for_repayment(emi, next_emi_date, interest_made, interest_future , remark)

                                # Update the loan data
                                loan["upcoming_emi_list"] = emi
                                

                                # Save updated data
                                liabilities_data[name]["loans"][loan_id] = loan  # Ensure the modified loan is saved back to liabilities_data
                                liabilities_data[name]["total_liabilities"] -= amount  # Adjust total liabilities

                                st.success("Repayment successful!")
                                save_data(liabilities, DATA_FILE)  # Save the entire structure
                        elif not confirm_repayment:
                            st.warning("Please confirm the repayment by checking the box.")

# Display liabilities
st.header("Current Liabilities")
if liabilities_data:
    for liability_name, details in liabilities_data.items():
        st.subheader(f"Name: {liability_name}")
        st.write(f"Active: {details['active']}")
        st.write(f"Number of Active Loans: {details['active_no_of_loan']}")
        st.write(f"Total Liabilities: {details['total_liabilities']}")
        st.write("Loans:")
        if details["loans"]:
            for loan_id, loan_details in details["loans"].items():
                st.write(f"- Loan ID {loan_id}:")
                st.json(loan_details)  # Use st.json() for better readability
        else:
            st.write("No loans added yet.")
else:
    st.write("No liabilities found.")
