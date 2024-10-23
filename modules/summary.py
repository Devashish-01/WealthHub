import streamlit as st
import pandas as pd
def summary_page():
    st.title("Financial Summary")

    # Fetching total liabilities, investments, and loans
    total_liabilities = st.session_state.liabilities_data['Amount'].sum() if 'liabilities_data' in st.session_state else 0
    total_investments = st.session_state.investments_data['Current Value'].sum() if 'investments_data' in st.session_state else 0
    total_loans = st.session_state.loans_data['Amount'].sum() if 'loans_data' in st.session_state else 0
    net_profit_loss = total_investments - total_liabilities - total_loans

    # Update session state with totals
    st.session_state.total_liabilities = total_liabilities
    st.session_state.total_investments = total_investments

    # Displaying summary metrics
    st.metric("Total Liabilities", f"₹{total_liabilities}")
    st.metric("Total Investments", f"₹{total_investments}")
    st.metric("Total Loans", f"₹{total_loans}")
    st.metric("Net Profit/Loss", f"₹{net_profit_loss}")

    # Comparison chart
    st.subheader("Liabilities, Investments & Loans Comparison")
    st.bar_chart(pd.DataFrame({
        'Liabilities': [total_liabilities],
        'Investments': [total_investments],
        'Loans': [total_loans]
    }))
