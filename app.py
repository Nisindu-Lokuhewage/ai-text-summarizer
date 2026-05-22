import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")

api_key = st.text_input("Enter your Gemini API Key:", type="password")

input_text = st.text_area("Paste your text here:", height=200)

if st.button("Summarize"):
    if api_key and input_text:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Summarize this: {input_text}")
        st.success(response.text)
    else:
        st.warning("Enter API key and text")
