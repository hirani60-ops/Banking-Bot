"""
HBDB Banking Bot - Streamlit Application
Simple, reliable, no startup dependencies
"""

import streamlit as st

# ============ PAGE CONFIG (MUST BE FIRST) ============
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ MAIN APP ============
st.title("🏦 HBDB Banking Bot")
st.markdown("*Ask your banking questions - Powered by Mistral AI*")

# Initialize session state
if "loaded_faqs" not in st.session_state:
    st.session_state.loaded_faqs = False
    st.session_state.df = None

# Load FAQs button
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("📚 Load FAQ Database", key="load_btn"):
        st.session_state.loaded_faqs = True

# Load the FAQ data
if st.session_state.loaded_faqs:
    try:
        import pandas as pd
        df = pd.read_csv("faqs.csv")
        st.session_state.df = df
        st.success(f"✅ Loaded {len(df)} FAQs from HBDB database")
    except FileNotFoundError:
        st.error("❌ FAQ file not found: faqs.csv")
        st.session_state.df = None
    except Exception as e:
        st.error(f"❌ Error loading FAQ file: {str(e)}")
        st.session_state.df = None

# Show interface only if FAQs are loaded
if st.session_state.df is not None:
    st.divider()
    
    # Input question
    user_question = st.text_input(
        "Ask me anything about HBDB banking:",
        placeholder="e.g., How do I open a savings account?"
    )
    
    if user_question:
        try:
            # Get API key
            api_key = None
            try:
                api_key = st.secrets.get("MISTRAL_API_KEY")
            except:
                import os
                api_key = os.getenv("MISTRAL_API_KEY")
            
            if not api_key:
                st.error("⚠️ API Key not configured in Streamlit Secrets")
            else:
                try:
                    import requests
                    
                    # Build FAQ context
                    faq_context = "\n\n".join([
                        f"Q: {row['Question']}\nA: {row['Answer']}"
                        for _, row in st.session_state.df.head(5).iterrows()
                    ])
                    
                    with st.spinner("🔍 Getting answer..."):
                        # Call Mistral API
                        response = requests.post(
                            "https://api.mistral.ai/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": "mistral-large-latest",
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": f"You are a helpful HBDB banking assistant. Answer based on these FAQs:\n\n{faq_context}\n\nIf the answer is not in the FAQs, provide helpful general information."
                                    },
                                    {"role": "user", "content": user_question}
                                ]
                            },
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            answer = result["choices"][0]["message"]["content"]
                            st.success("✅ Answer:")
                            st.write(answer)
                        else:
                            st.error(f"API Error: {response.status_code}")
                            st.write(response.text)
                
                except ImportError:
                    st.error("requests library not installed")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Show FAQ list
    if st.checkbox("📋 View All FAQs"):
        st.subheader("HBDB FAQ Database")
        for idx, row in st.session_state.df.iterrows():
            with st.container():
                st.write(f"**Q: {row['Question']}**")
                st.write(f"{row['Answer']}")
                st.divider()

else:
    st.info("👆 Click 'Load FAQ Database' button above to get started!")








