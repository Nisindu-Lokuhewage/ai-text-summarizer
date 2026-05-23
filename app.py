import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")

st.title("🤖 AI Text Summarizer")
st.markdown("Powered by **Google Gemini AI**")

# Try to get API key from environment variable (Render) first
# If not found, fall back to user input (for local testing)
api_key = os.environ.get("GEMINI_API_KEY", "")

# If no environment variable, ask user to input
if not api_key:
    api_key = st.text_input("🔑 **Google Gemini API Key**", type="password", 
                           help="Get free key from Google AI Studio")
    
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key to continue")
        st.stop()

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, 
                         placeholder="Paste your text here...")

# Summary length
length = st.radio(
    "📏 **Summary length**",
    options=["Short (2-3 sentences)", "Medium (4-5 sentences)", "Detailed (6-8 sentences)"],
    index=0
)

# Map length to parameters
settings = {
    "Short (2-3 sentences)": {"prompt": "2-3 sentences", "tokens": 100},
    "Medium (4-5 sentences)": {"prompt": "4-5 sentences", "tokens": 180},
    "Detailed (6-8 sentences)": {"prompt": "6-8 sentences", "tokens": 300}
}

if st.button("✨ **Summarize with Gemini**", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to summarize")
    else:
        with st.spinner("🧠 Gemini AI is thinking..."):
            try:
                # Google Gemini API call
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                
                prompt = f"""Summarize the following text in {settings[length]['prompt']}. Keep the key information.

Text: {input_text}

Summary:"""
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.5,
                        "maxOutputTokens": settings[length]["tokens"]
                    }
                }
                
                response = requests.post(url, json=payload, timeout=30)
                result = response.json()
                
                if "candidates" in result:
                    summary = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    st.success("✅ **Gemini Summary**")
                    st.write(summary)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Original", f"{len(input_text.split())} words")
                    with col2:
                        st.metric("Summary", f"{len(summary.split())} words")
                else:
                    error = result.get("error", {}).get("message", "Unknown error")
                    st.error(f"Gemini API Error: {error}")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

st.markdown("---")
st.markdown("💡 **Note:** Your API key is securely stored on Render")
