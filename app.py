import streamlit as st

st.set_page_config(page_title="Banking Bot", layout="wide")
st.title("🏦 HBDB Banking Bot")
st.write("Testing if Streamlit Cloud works...")

# Test: Load FAQs
if st.button("Load FAQs"):
    import pandas as pd
    try:
        df = pd.read_csv("faqs.csv")
        st.success(f"✅ Loaded {len(df)} FAQs")
        st.write(df.head(3))
    except Exception as e:
        st.error(f"Error: {e}")

# Test: Ask question
st.divider()
question = st.text_input("Ask a question:")
if question:
    st.write(f"You asked: {question}")
    try:
        import requests
        api_key = st.secrets["MISTRAL_API_KEY"]
        
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "mistral-large-latest",
                "messages": [{"role": "user", "content": question}]
            }
        )
        
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Answer:")
            st.write(answer)
        else:
            st.error(f"API Error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.divider()
st.write("**STATUS:** If you see this, Streamlit Cloud is working! ✅")
