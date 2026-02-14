"""
HBDB Banking Bot - Production Version
A robust, reliable banking FAQ chatbot powered by Mistral AI
"""

import streamlit as st
import pandas as pd
import requests
import os
from typing import Optional, List, Dict

# ============================================================================
# PAGE CONFIGURATION (MUST BE FIRST - DO NOT MOVE)
# ============================================================================
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "HBDB Banking Bot - Powered by Mistral AI"
    }
)

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================
CSV_FILE = "faqs.csv"
MODEL_NAME = "mistral-large-latest"
API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
REQUEST_TIMEOUT = 30

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "faqs_loaded" not in st.session_state:
    st.session_state.faqs_loaded = False
    st.session_state.df = None
    st.session_state.error_message = None
    st.session_state.api_key = None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_resource
def get_api_key() -> Optional[str]:
    """
    Safely retrieve API key from Streamlit Secrets or environment variables.
    Order of precedence:
    1. Streamlit Secrets (for Streamlit Cloud)
    2. Environment variables (for local development)
    """
    try:
        # Try Streamlit secrets first (works on Streamlit Cloud)
        return st.secrets.get("MISTRAL_API_KEY")
    except Exception:
        pass
    
    # Fallback to environment variable
    return os.getenv("MISTRAL_API_KEY")

def load_faq_database() -> Optional[pd.DataFrame]:
    """
    Load FAQ database from CSV file.
    Returns DataFrame if successful, None otherwise.
    """
    try:
        if not os.path.exists(CSV_FILE):
            raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")
        
        df = pd.read_csv(CSV_FILE)
        
        # Validate required columns
        if "Question" not in df.columns or "Answer" not in df.columns:
            raise ValueError("CSV must contain 'Question' and 'Answer' columns")
        
        # Remove any null rows
        df = df.dropna(subset=["Question", "Answer"])
        
        return df
    
    except FileNotFoundError as e:
        st.session_state.error_message = f"❌ File Error: {str(e)}"
        return None
    except ValueError as e:
        st.session_state.error_message = f"❌ Format Error: {str(e)}"
        return None
    except Exception as e:
        st.session_state.error_message = f"❌ Unexpected Error: {str(e)}"
        return None

def get_faq_context(df: pd.DataFrame, num_faqs: int = 5) -> str:
    """
    Build FAQ context string from top N FAQs.
    """
    faq_list = []
    for idx, row in df.head(num_faqs).iterrows():
        faq_list.append(f"Q: {row['Question']}\nA: {row['Answer']}")
    
    return "\n\n".join(faq_list)

def query_mistral_api(question: str, faq_context: str, api_key: str) -> Optional[str]:
    """
    Send query to Mistral API and return response.
    Handles errors gracefully.
    """
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful HBDB banking assistant. "
                        "You answer customer questions about banking services based on the provided FAQs. "
                        "Be concise, friendly, and professional. "
                        "If the answer is not in the FAQs, acknowledge this and provide helpful general banking information. "
                        "Always recommend contacting HBDB customer service for complex issues.\n\n"
                        f"HBDB FAQs:\n{faq_context}"
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code} - {response.text[:200]}"
    
    except requests.Timeout:
        return "Error: API request timed out. Please try again."
    except requests.RequestException as e:
        return f"Network Error: {str(e)}"
    except KeyError:
        return "Error: Unexpected API response format."
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# MAIN UI LAYOUT
# ============================================================================

# Header
st.title("🏦 HBDB Banking Bot")
st.markdown(
    "**Your AI-powered assistant for banking questions**  \n"
    "Ask questions about HBDB services - Powered by Mistral AI"
)

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This chatbot uses Mistral Large AI to answer your banking questions "
        "based on HBDB's FAQ database."
    )
    
    # API Key Status
    api_key = get_api_key()
    if api_key:
        st.success("✅ API Key Configured")
    else:
        st.warning("⚠️ API Key Not Found")
        st.caption("Add MISTRAL_API_KEY to Streamlit Secrets")

# ============================================================================
# LOAD FAQ DATABASE BUTTON
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("📚 Load FAQs", key="load_faq_btn", type="primary"):
        with st.spinner("Loading FAQ database..."):
            df = load_faq_database()
            if df is not None:
                st.session_state.df = df
                st.session_state.faqs_loaded = True
                st.success(f"✅ Loaded {len(df)} FAQs")
            else:
                st.error(st.session_state.error_message or "Failed to load FAQs")

# ============================================================================
# MAIN CHAT INTERFACE (ONLY IF FAQs LOADED)
# ============================================================================

if st.session_state.faqs_loaded and st.session_state.df is not None:
    st.divider()
    
    # Question Input
    user_question = st.text_input(
        "Ask your question:",
        placeholder="e.g., How do I open a new account? What's the minimum balance?",
        help="Type your banking question here"
    )
    
    # Process Question
    if user_question:
        api_key = get_api_key()
        
        if not api_key:
            st.error(
                "❌ API Key not configured. "
                "Please add MISTRAL_API_KEY to Streamlit Secrets."
            )
        else:
            # Get FAQ context
            faq_context = get_faq_context(st.session_state.df, num_faqs=5)
            
            # Query API
            with st.spinner("🔍 Getting answer from Mistral AI..."):
                answer = query_mistral_api(user_question, faq_context, api_key)
            
            # Display answer
            if answer:
                st.success("✅ Answer:")
                st.write(answer)
            else:
                st.error("Failed to get answer.")
    
    st.divider()
    
    # FAQ Viewer
    if st.checkbox("📋 Show FAQ Database"):
        st.subheader("HBDB Banking FAQs")
        
        # Search functionality
        search_term = st.text_input(
            "Search FAQs:",
            placeholder="Search questions or answers...",
            help="Filter FAQs by keyword"
        )
        
        # Filter FAQs
        filtered_df = st.session_state.df
        if search_term:
            mask = (
                st.session_state.df["Question"].str.contains(
                    search_term, case=False, na=False
                ) |
                st.session_state.df["Answer"].str.contains(
                    search_term, case=False, na=False
                )
            )
            filtered_df = st.session_state.df[mask]
        
        # Display FAQs
        if len(filtered_df) == 0:
            st.info("No FAQs found matching your search.")
        else:
            for idx, (_, row) in enumerate(filtered_df.iterrows(), 1):
                with st.container():
                    col1, col2 = st.columns([0.8, 0.2]
)
                    with col1:
                        st.write(f"**{idx}. {row['Question']}**")
                    st.write(f"{row['Answer']}")
                    st.divider()

else:
    # Welcome message when FAQs not loaded
    st.info(
        "👆 Click the '📚 Load FAQs' button above to get started with the HBDB Banking Bot!"
    )
    
    st.markdown("""
    ### How it works:
    1. **Load FAQs** - Click the button to load the HBDB FAQ database
    2. **Ask a Question** - Type your banking question in the input field
    3. **Get Answer** - The AI assistant will provide an answer based on FAQs
    4. **Browse FAQs** - View and search the complete FAQ database
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption(
    "🏦 HBDB Banking Bot | Powered by Mistral AI Large | "
    f"FAQs: {len(st.session_state.df) if st.session_state.df is not None else 'Not loaded'}"
)
