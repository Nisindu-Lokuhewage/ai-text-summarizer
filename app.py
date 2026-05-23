import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")

st.title("🤖 AI Text Summarizer")
st.markdown("Powered by **Google Gemini 3.5 Flash** (Free Tier)")

# Gemini API key (get from https://aistudio.google.com)
api_key = st.text_input("🔑 **Google Gemini API Key**", type="password", 
                       help="Get free key from Google AI Studio")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, 
                         placeholder="Paste your text here...")

# Summary length - USING RADIO BUTTONS INSTEAD (more reliable)
length = st.radio(
    "📏 **Summary length**",
    options=["Short (2-3 sentences)", "Medium (4-5 sentences)", "Detailed (6-8 sentences)"],
    index=0  # 0 = Short selected by default
)

# Map length to max_tokens
token_map = {
    "Short (2-3 sentences)": 80,
    "Medium (4-5 sentences)": 150,
    "Detailed (6-8 sentences)": 250
}

# Map length for prompt
prompt_map = {
    "Short (2-3 sentences)": "2-3 sentences",
    "Medium (4-5 sentences)": "4-5 sentences",
    "Detailed (6-8 sentences)": "6-8 sentences"
}

if st.button("✨ **Summarize with Gemini**", type="primary"):
    if not api_key:
        st.error("❌ Please enter your Gemini API key")
    elif not input_text.strip():
        st.warning("⚠️ Please enter text to summarize")
    else:
        with st.spinner("🧠 Gemini AI is thinking..."):
            try:
                # ✅ UPDATED: Using gemini-3.5-flash (the current free-tier model)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Summarize this text in {prompt_map[length]}. Keep key facts only.\n\nText: {input_text}\n\nSummary:"
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": token_map[length]
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
                    st.info("💡 Make sure you've enabled the Gemini API in Google Cloud Console")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

st.markdown("---")
st.markdown("Get your free Gemini API key at [Google AI Studio](https://aistudio.google.com)")
