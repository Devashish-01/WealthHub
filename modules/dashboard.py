import streamlit as st
import pandas as pd

def dashboard_page():
    st.title("Dashboard Overview")

    # Calculate total liabilities and investments
    total_liabilities = st.session_state.get('total_liabilities', 0)
    total_investments = st.session_state.get('total_investments', 0)
    total_profit = total_investments - total_liabilities

    # Display key statistics
    st.metric("Total Liabilities", f"₹{total_liabilities}")
    st.metric("Total Investments", f"₹{total_investments}")
    st.metric("Profit/Loss", f"₹{total_profit}")

    # Find the nearest deadline from liabilities or loans
    nearest_deadline = None
    if 'liabilities_data' in st.session_state:
        nearest_liability = st.session_state.liabilities_data['Deadline'].min() if not st.session_state.liabilities_data.empty else None
        nearest_deadline = nearest_liability

    if 'loans_data' in st.session_state:
        nearest_loan = st.session_state.loans_data['Deadline'].min() if not st.session_state.loans_data.empty else None
        if nearest_deadline:
            nearest_deadline = min(nearest_deadline, nearest_loan)
        else:
            nearest_deadline = nearest_loan

    if nearest_deadline:
        st.warning(f"Nearest Deadline: {nearest_deadline}")

    # Visualization placeholder
    st.subheader("Visualization of Liabilities vs. Investments")
    st.bar_chart(pd.DataFrame({
        'Liabilities': [total_liabilities],
        'Investments': [total_investments]
    }))
