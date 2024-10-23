import streamlit as st

def loans_page():
    st.title("Loans Overview")

    st.write("""
    Select the loan type from the sidebar to add, view, or manage specific loans.
    """)

    # Display current loans
    st.subheader("Current Loans")
    if not st.session_state.loans_data.empty:
        st.data_editor(st.session_state.loans_data, height=300)
    else:
        st.info("No loans added yet.")
