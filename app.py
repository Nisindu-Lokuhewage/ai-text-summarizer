import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")
st.markdown("Powered by **Hugging Face Free AI Models** - No API key needed!")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, placeholder="Paste or type your text here...")

# Summary length option
length = st.select_slider("📏 **Summary length**", options=["Short", "Medium", "Detailed"], value="Short")

length_map = {
    "Short": "2-3 sentences",
    "Medium": "4-5 sentences", 
    "Detailed": "6-8 sentences"
}

# Free API endpoint (no key needed)
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def summarize_text(text, max_length):
    """Send text to Hugging Face's free summarization API"""
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": 30,
            "do_sample": False
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result[0]['summary_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

if st.button("✨ **Summarize**", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to summarize")
    else:
        # Set max length based on user choice
        length_settings = {
            "Short": 150,
            "Medium": 250,
            "Detailed": 400
        }
        
        with st.spinner("🤖 AI is reading and summarizing your text..."):
            try:
                summary = summarize_text(input_text, length_settings[length])
                
                st.success("✅ **Summary Ready!**")
                st.write(summary)
                
                # Show stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original", f"{len(input_text.split())} words")
                with col2:
                    st.metric("Summary", f"{len(summary.split())} words")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("💡 The free API might be busy. Wait 10 seconds and try again.")

st.markdown("---")
st.markdown("Powered by **Facebook BART-large-CNN** on Hugging Face (100% Free)")
