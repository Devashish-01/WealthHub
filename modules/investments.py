import streamlit as st
import pandas as pd

def investments_page():
    st.title("Manage Investments")

    with st.form("add_investment", clear_on_submit=True):
        st.subheader("Add New Investment")

        # Select investment type
        investment_type = st.selectbox("Investment Type", ["Real Estate", "Stocks", "Gold", "Others"])
        asset = st.text_input("Asset/Property Name", placeholder="Enter asset or property name")
        initial_amount = st.number_input("Initial Amount", min_value=0.0, step=0.01)
        deadline = st.date_input("Realization Deadline")
        remark = st.text_area("Remark", placeholder="Enter additional notes or comments")

        # Conditional fields based on investment type
        if investment_type == "Stocks":
            current_price = st.number_input("Current Price per Share", min_value=0.0, step=0.01)
            expected_price = st.number_input("Expected Price per Share", min_value=0.0, step=0.01)
            volume = st.number_input("Volume (Number of Shares)", min_value=0, step=1)

            # Calculate total value and expected return
            current_value = current_price * volume
            expected_return = (expected_price - current_price) * volume

            st.write(f"Current Value: ₹{current_value:.2f}")
            st.write(f"Expected Return: ₹{expected_return:.2f}")

        elif investment_type == "Real Estate":
            area = st.number_input("Area (in sq ft)", min_value=0.0, step=0.01)
            current_value = st.number_input("Current Market Value", min_value=0.0, step=0.01)
            expected_value = st.number_input("Expected Market Value", min_value=0.0, step=0.01)

            expected_return = expected_value - current_value

            st.write(f"Expected Return: ₹{expected_return:.2f}")

        elif investment_type == "Gold":
            weight = st.number_input("Weight (in grams)", min_value=0.0, step=0.01)
            current_price_per_gram = st.number_input("Current Price per Gram", min_value=0.0, step=0.01)
            expected_price_per_gram = st.number_input("Expected Price per Gram", min_value=0.0, step=0.01)

            current_value = weight * current_price_per_gram
            expected_return = weight * (expected_price_per_gram - current_price_per_gram)

            st.write(f"Current Value: ₹{current_value:.2f}")
            st.write(f"Expected Return: ₹{expected_return:.2f}")

        else:
            current_value = st.number_input("Current Value", min_value=0.0, step=0.01)
            expected_return = st.number_input("Expected Return", min_value=0.0, step=0.01)

        # Submit button to add investment entry
        submit = st.form_submit_button("Add Investment")
        if submit:
            try:
                investment_entry = {
                    'Investment Type': investment_type,
                    'Asset': asset,
                    'Initial Amount': initial_amount,
                    'Current Value': current_value,
                    'Expected Return': expected_return,
                    'Deadline': deadline,
                    'Remark': remark
                }

                if investment_type == "Stocks":
                    investment_entry.update({'Volume': volume, 'Current Price': current_price, 'Expected Price': expected_price})
                elif investment_type == "Real Estate":
                    investment_entry['Area'] = area
                elif investment_type == "Gold":
                    investment_entry.update({'Weight': weight, 'Current Price per Gram': current_price_per_gram, 'Expected Price per Gram': expected_price_per_gram})

                new_entry = pd.DataFrame([investment_entry])
                st.session_state.investments_data = pd.concat([st.session_state.investments_data, new_entry], ignore_index=True)
                st.success(f"{investment_type} Investment added successfully!")

            except Exception as e:
                st.error(f"An error occurred while adding the investment: {e}")

    # Display current investments
    st.subheader("Current Investments")
    if not st.session_state.investments_data.empty:
        st.data_editor(st.session_state.investments_data, height=400)
    else:
        st.info("No investments added yet.")
