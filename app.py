import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")
st.markdown("Powered by **OpenRouter Free AI**")

# API Key input (free from openrouter.ai)
api_key = st.text_input("🔑 **OpenRouter API Key**", type="password", help="Get free key from https://openrouter.ai/keys")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, placeholder="Paste your text here...")

# Summary length
length = st.select_slider("📏 **Summary length**", options=["Short", "Medium", "Detailed"], value="Short")

length_prompt = {
    "Short": "in 2-3 sentences",
    "Medium": "in 4-5 sentences",
    "Detailed": "in 6-8 sentences"
}

if st.button("✨ **Summarize**", type="primary"):
    if not api_key:
        st.error("❌ Please enter your OpenRouter API key")
    elif not input_text.strip():
        st.warning("⚠️ Please enter some text to summarize")
    else:
        with st.spinner("🤖 AI is summarizing..."):
            try:
                # USING A CONFIRMED WORKING FREE MODEL
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": "google/gemma-4-31b-it:free",  # ✅ Confirmed working free model
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Summarize the following text {length_prompt[length]}. Keep the key information.\n\nText: {input_text}\n\nSummary:"
                            }
                        ]
                    })
                )
                
                result = response.json()
                
                if "choices" in result:
                    summary = result["choices"][0]["message"]["content"]
                    
                    st.success("✅ **Summary Ready!**")
                    st.write(summary)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Original", f"{len(input_text.split())} words")
                    with col2:
                        st.metric("Summary", f"{len(summary.split())} words")
                else:
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    st.error(f"API Error: {error_msg}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Get your free API key at [OpenRouter](https://openrouter.ai/keys)")
