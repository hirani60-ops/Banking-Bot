import streamlit as st

st.title("🏦 HBDB Banking Bot")
st.write("✅ App is running!")

if st.button("Load FAQs"):
    import pandas as pd
    df = pd.read_csv("faqs.csv")
    st.success(f"Loaded {len(df)} FAQs")

st.text_input("Ask:", key="q")
if st.session_state.q:
    import requests
    api_key = st.secrets["MISTRAL_API_KEY"]
    r = requests.post("https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "mistral-large-latest", "messages": [{"role": "user", "content": st.session_state.q}]})
    st.write(r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else r.text)
