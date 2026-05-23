import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")

st.title("🤖 AI Text Summarizer")
st.markdown("Powered by **Google Gemini 3.5 Flash** (Free Tier)")

# Gemini API key
api_key = st.text_input("🔑 **Google Gemini API Key**", type="password", 
                       help="Get free key from Google AI Studio")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, 
                         placeholder="Paste your text here...")

# Summary length
length = st.radio(
    "📏 **Summary length**",
    options=["Short", "Medium", "Detailed"],
    index=0
)

# Map length settings
settings = {
    "Short": {"sentences": "2-3 sentences", "tokens": 100},
    "Medium": {"sentences": "4-5 sentences", "tokens": 180},
    "Detailed": {"sentences": "6-8 sentences", "tokens": 300}
}

if st.button("✨ **Summarize with Gemini**", type="primary"):
    if not api_key:
        st.error("❌ Please enter your Gemini API key")
    elif not input_text.strip():
        st.warning("⚠️ Please enter text to summarize")
    else:
        with st.spinner("🧠 Gemini AI is thinking..."):
            try:
                # Improved prompt for better summaries
                prompt = f"""You are a helpful summarization assistant. Summarize the text below in {settings[length]['sentences']}. 

IMPORTANT RULES:
- Write complete, readable sentences
- Keep the most important facts
- Don't be too short - use {settings[length]['sentences']} as a guide
- Don't add new information not in the text

Text to summarize:
{input_text}

Summary:"""
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.5,
                        "maxOutputTokens": settings[length]["tokens"],
                        "topP": 0.9
                    }
                }
                
                response = requests.post(url, json=payload, timeout=30)
                result = response.json()
                
                if "candidates" in result:
                    summary = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Clean up the summary if needed
                    summary = summary.strip()
                    if len(summary.split()) < 10 and len(input_text.split()) > 30:
                        st.warning("⚠️ Summary was too short. Click Summarize again - the AI sometimes needs a second try.")
                    
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
st.markdown("💡 **Pro tip:** If the summary is too short, click Summarize again - free tier sometimes needs a second try.")
st.markdown("Get your free Gemini API key at [Google AI Studio](https://aistudio.google.com)")
