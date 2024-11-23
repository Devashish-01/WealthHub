import os
import json
from datetime import date, datetime, timedelta

import streamlit as st
from utils import (
    security_check, 
    get_next_id, 
    previous_emi_date, 
    remove_further_emi, 
    change_emi_for_repayment
)

class RepaymentManager:
    def __init__(self, data_file="liabilities_data.json"):
        self.DATA_FILE = data_file
        self.liabilities = self.load_data()
        self.liabilities_data = self.liabilities.get("liabilities", {})

    def load_data(self):
        """
        Enhanced data loading with multiple error handling strategies.
        """
        try:
            if not os.path.exists(self.DATA_FILE):
                return self._create_default_structure()
            
            with open(self.DATA_FILE, "r") as file:
                data = json.load(file)
                # Additional validation
                if not isinstance(data, dict) or "liabilities" not in data:
                    return self._create_default_structure()
                return data
        except (json.JSONDecodeError, PermissionError):
            st.error(f"Could not read {self.DATA_FILE}. Using default structure.")
            return self._create_default_structure()

    def _create_default_structure(self):
        """Create a default data structure if no valid data exists."""
        return {"liabilities": {}, "metadata": {"last_updated": str(datetime.now())}}

    def validate_repayment_inputs(self, name, loan_id, amount):
        """
        Comprehensive input validation with detailed error messages.
        """
        # Lender validation
        if name not in self.liabilities_data:
            st.error(f"Lender '{name}' not found in records.")
            return None

        # Loan validation
        lender_loans = self.liabilities_data[name].get("loans", {})
        if loan_id not in lender_loans:
            st.error(f"Loan ID '{loan_id}' not found for lender '{name}'.")
            return None

        # Amount validation
        loan = lender_loans[loan_id]
        if amount <= 0:
            st.error("Repayment amount must be positive.")
            return None
        
        if amount > loan.get("current_principle", 0):
            st.error(f"Repayment amount exceeds remaining loan balance of {loan.get('current_principle', 0)}")
            return None

        return loan

    def process_repayment(self, loan, amount, remark=""):
        """
        Comprehensive repayment processing with advanced tracking.
        """
        repayment_date = date.today()
        emi_list = loan.get("upcoming_emi_list", [])

        try:
            previous_emi = previous_emi_date(emi_list)
            days_since_last_emi = (repayment_date - previous_emi).days
            
            # Advanced interest calculation
            interest_made = (amount * loan["interest_rate"] * days_since_last_emi) / (30 * 100)
            interest_future = (loan["current_principle"] - amount) * loan["interest_rate"] / 100

            # Security and processing
            if not security_check(amount, "repayment amount"):
                st.error("Security check failed. Transaction aborted.")
                return False

            # Update loan details
            loan["current_principle"] -= amount
            loan["total_paid"] = loan.get("total_paid", 0) + amount

            repayment_record = {
                "amount": amount,
                "date": str(repayment_date),
                "remark": remark,
                "days_since_last_emi": days_since_last_emi
            }

            # Handle loan completion
            if loan["current_principle"] <= 0:
                loan["status"] = "COMPLETED"
                loan["completed_date"] = str(repayment_date)
                emi_list = remove_further_emi(emi_list)
            else:
                emi_list = change_emi_for_repayment(
                    emi_list, 
                    previous_emi + timedelta(days=loan["interest_payment_interval_months"] * 30),
                    interest_made, 
                    interest_future
                )

            loan["upcoming_emi_list"] = emi_list
            loan["repayment_history"].append(repayment_record)

            return True

        except Exception as e:
            st.error(f"Repayment processing error: {e}")
            return False

    def run_repayment_workflow(self):
        """
        Interactive Streamlit workflow for repayment.
        """
        st.title("Smart Repayment Management")
        
        # Lender selection with autocomplete
        available_lenders = list(self.liabilities_data.keys())
        name = st.selectbox("Select Lender", available_lenders)

        if name:
            # Loan selection
            lender_loans = self.liabilities_data[name].get("loans", {})
            loan_ids = list(lender_loans.keys())
            loan_id = st.selectbox("Select Loan", loan_ids)

            if loan_id:
                # Amount input with slider and validation
                loan = lender_loans[loan_id]
                max_repayment = loan.get("current_principle", 0)
                amount = st.slider(
                    "Repayment Amount", 
                    min_value=0.0, 
                    max_value=float(max_repayment), 
                    step=100.0
                )

                remark = st.text_input("Optional Remark")

                if st.button("Confirm Repayment"):
                    validated_loan = self.validate_repayment_inputs(name, loan_id, amount)
                    if validated_loan:
                        if self.process_repayment(validated_loan, amount, remark):
                            st.success("Repayment Processed Successfully!")
                            self.save_data()
                        else:
                            st.error("Repayment Failed. Please try again.")

    def save_data(self):
        """Enhanced data saving with metadata tracking."""
        self.liabilities["metadata"] = {
            "last_updated": str(datetime.now()),
            "total_lenders": len(self.liabilities_data),
            "total_active_loans": sum(
                len(lender.get("loans", {})) 
                for lender in self.liabilities_data.values()
            )
        }
        
        try:
            with open(self.DATA_FILE, "w") as file:
                json.dump(self.liabilities, file, indent=4)
            st.sidebar.success("Data saved with enhanced tracking!")
        except Exception as e:
            st.error(f"Data saving failed: {e}")

def main():
    app = RepaymentManager()
    app.run_repayment_workflow()

if __name__ == "__main__":
    main()