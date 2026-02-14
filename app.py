import streamlit as st

st.title("🏦 HBDB Banking Bot")

# Initialize session state
if "faqs_loaded" not in st.session_state:
    st.session_state.faqs_loaded = False
    st.session_state.df = None

# Load FAQs
if st.button("📚 Load FAQ Database", use_container_width=True):
    try:
        import pandas as pd
        df = pd.read_csv("faqs.csv")
        st.session_state.df = df
        st.session_state.faqs_loaded = True
        st.success(f"✅ Loaded {len(df)} FAQs")
    except Exception as e:
        st.error(f"Error loading FAQs: {e}")

# Ask question only if FAQs are loaded
if st.session_state.faqs_loaded:
    st.divider()
    question = st.text_input("Ask a banking question:", placeholder="How do I open a savings account?")
    
    if question:
        try:
            import requests
            api_key = st.secrets["MISTRAL_API_KEY"]
            
            # Build FAQ context
            faq_context = "\n\n".join([
                f"Q: {row['Question']}\nA: {row['Answer']}"
                for _, row in st.session_state.df.iterrows()
            ])
            
            # Call Mistral API with FAQ context
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "mistral-large-latest",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are an HBDB banking assistant. Answer questions based on these FAQs:\n\n{faq_context}"
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
            )
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                st.success("✅ Answer:")
                st.write(answer)
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("👆 Click '📚 Load FAQ Database' to start")
