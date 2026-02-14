import streamlit as st

st.set_page_config(page_title="HBDB Bot", page_icon="🏦")
st.title("HBDB Banking Bot")

st.write("Hello! The app is running.")

# Only read CSV if user interacts
if st.button("Load FAQs"):
    try:
        import pandas as pd
        df = pd.read_csv("hbdb_banking_faqs (2) (1).csv")
        st.success(f"Loaded {len(df)} FAQs!")
    except Exception as e:
        st.error(f"Error: {e}")







