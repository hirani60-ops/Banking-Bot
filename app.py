"""
HBDB Banking Bot - Ultra-Safe Version
Zero imports at startup - guaranteed to load on Streamlit Cloud
"""

import streamlit as st
# PAGE CONFIG ONLY
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide"
)

# DISPLAY HEADER IMMEDIATELY
st.title("🏦 HBDB Banking Bot")
st.markdown("**Your AI-powered banking assistant**")

# SESSION STATE
if "faqs_loaded" not in st.session_state:
    st.session_state.faqs_loaded = False
    st.session_state.df = None

# SIDEBAR
with st.sidebar:
    st.header("ℹ️ About")
    st.write("Ask banking questions - Powered by Mistral AI")
    try:
        api_key = st.secrets.get("MISTRAL_API_KEY")
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ API Key not found")
    except:
        st.warning("⚠️ No API Key")

# MAIN
if st.button("📚 Load FAQ Database", use_container_width=True, type="primary"):
    try:
        import pandas as pd
        import os
        csv_file = "faqs.csv"
        if not os.path.exists(csv_file):
            st.error(f"❌ File not found: {csv_file}")
        else:
            df = pd.read_csv(csv_file)
            if len(df) > 0:
                st.session_state.df = df
                st.session_state.faqs_loaded = True
                st.success(f"✅ Loaded {len(df)} FAQs")
            else:
                st.error("❌ CSV is empty")
    except Exception as e:
        st.error(f"❌ Error: {str(e)[:100]}")

if st.session_state.faqs_loaded and st.session_state.df is not None:
    st.divider()
    question = st.text_input("Ask your question:", placeholder="How do I open an account?")
    
    if question:
        try:
            api_key = st.secrets.get("MISTRAL_API_KEY")
            if not api_key:
                st.error("❌ API Key not configured")
            else:
                import requests
                faq_text = "\n\n".join([
                    f"Q: {row['Question']}\nA: {row['Answer']}"
                    for _, row in st.session_state.df.head(5).iterrows()
                ])
                with st.spinner("Getting answer..."):
                    response = requests.post(
                        "https://api.mistral.ai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "mistral-large-latest",
                            "messages": [
                                {"role": "system", "content": f"You are HBDB banking assistant. Answer based on FAQs:\n{faq_text}"},
                                {"role": "user", "content": question}
                            ]
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        answer = response.json()["choices"][0]["message"]["content"]
                        st.success("✅ Answer:")
                        st.write(answer)
                    else:
                        st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:100]}")
    
    st.divider()
    if st.checkbox("📋 View FAQ Database"):
        search = st.text_input("Search:", placeholder="Search...")
        df = st.session_state.df
        if search:
            mask = (df["Question"].str.contains(search, case=False, na=False) | df["Answer"].str.contains(search, case=False, na=False))
            df = df[mask]
        if len(df) == 0:
            st.info("No FAQs found")
        else:
            for idx, (_, row) in enumerate(df.iterrows(), 1):
                st.write(f"**{idx}. {row['Question']}**")
                st.write(row['Answer'])
                st.divider()
else:
    st.info("👆 Click '📚 Load FAQ Database' to start")
