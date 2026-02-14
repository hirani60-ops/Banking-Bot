import streamlit as st
import pandas as pd
from mistralai import Mistral
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Mistral client
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    st.error("MISTRAL_API_KEY not found. Please set it in .env file or as an environment variable.")
    st.stop()

client = Mistral(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load FAQ data
@st.cache_data
def load_faq_data():
    """Load FAQ data from CSV file"""
    try:
        df = pd.read_csv("hbdb_banking_faqs (2) (1).csv")
        return df
    except FileNotFoundError:
        st.error("FAQ CSV file not found. Please ensure 'hbdb_banking_faqs (2) (1).csv' is in the same directory.")
        return None

# Main application
def main():
    # Header
    st.title("🏦 HBDB Banking Bot")
    st.markdown("*Your AI-powered assistant for banking questions*")
    
    # Load FAQ data
    faq_df = load_faq_data()
    
    if faq_df is None:
        return
    
    # Sidebar information
    with st.sidebar:
        st.header("About")
        st.markdown("""
        ### HBDB Banking Assistant
        
        This bot uses **Mistral Large AI** to answer your banking questions based on HBDB's FAQs.
        
        **Features:**
        - Answer FAQ questions using AI
        - Provide helpful banking information
        - Available 24/7
        
        **Currently loaded FAQs:** {}
        """.format(len(faq_df)))
    
    # Create context from FAQ data
    faq_context = "Here are the banking FAQs:\n\n"
    for idx, row in faq_df.iterrows():
        faq_context += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    
    # User input
    user_question = st.text_input(
        "Ask me anything about HBDB banking:",
        placeholder="e.g., How do I open a savings account?"
    )
    
    if user_question:
        with st.spinner("Searching for the best answer..."):
            try:
                # Create message for Mistral
                messages = [
                    {
                        "role": "system",
                        "content": f"""You are a helpful banking assistant for HBDB. 
Use the following FAQs to answer user questions. If the answer is not in the FAQs, 
provide helpful general banking information and suggest contacting HBDB customer service.

{faq_context}"""
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ]
                
                # Call Mistral API
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                # Display response
                st.success("Answer found!")
                st.markdown("### Response:")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display FAQ section
    with st.expander("📋 View All FAQs", expanded=False):
        st.markdown("### Banking FAQs")
        for idx, row in faq_df.iterrows():
            with st.container():
                st.markdown(f"**Q: {row['Question']}**")
                st.markdown(f"*A: {row['Answer']}*")
                st.divider()

if __name__ == "__main__":
    main()
