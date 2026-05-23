import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")

st.title("🤖 AI Text Summarizer")
st.markdown("Powered by **Facebook BART** - Professional AI Summarization")

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
    "Short (2-3 sentences)": {"min": 30, "max": 80},
    "Medium (4-5 sentences)": {"min": 50, "max": 150},
    "Detailed (6-8 sentences)": {"min": 80, "max": 250}
}

@st.cache_data(ttl=60)
def get_summary(text, min_len, max_len):
    """Call Hugging Face's free summarization API"""
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_len,
            "min_length": min_len,
            "do_sample": False,
            "clean_up_tokenization_spaces": True
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('summary_text', str(result))
        return str(result)
    else:
        return None

if st.button("✨ **Summarize with AI**", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to summarize")
    else:
        with st.spinner("🤖 AI is analyzing and summarizing..."):
            try:
                summary = get_summary(
                    input_text, 
                    settings[length]["min"], 
                    settings[length]["max"]
                )
                
                if summary:
                    st.success("✅ **AI Summary**")
                    st.write(summary)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Original", f"{len(input_text.split())} words")
                    with col2:
                        st.metric("Summary", f"{len(summary.split())} words")
                else:
                    st.error("⚠️ API is busy. Free tier has rate limits. Please wait 10 seconds and try again.")
                    
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. The free API is busy. Try again in 15 seconds.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("💡 The free API has rate limits. Click 'Summarize' again in a few seconds.")

st.markdown("---")
st.markdown("💡 **Note:** Using free Hugging Face API. If busy, wait 10 seconds and try again.")
st.markdown("Powered by **Facebook BART-large-CNN** - A professional summarization model")
