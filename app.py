import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")
st.markdown("Powered by **Free AI** - Just paste your text!")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200, placeholder="Paste or type your text here...")

# Summary length option
length = st.select_slider("📏 **Summary length**", options=["Short", "Medium", "Detailed"], value="Short")

if st.button("✨ **Summarize**", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to summarize")
    else:
        with st.spinner("🤖 Summarizing..."):
            try:
                # Use a different free API that doesn't require API key
                # This is a public summarization endpoint
                
                payload = {
                    "text": input_text,
                    "max_length": 200 if length == "Short" else 300 if length == "Medium" else 500,
                    "min_length": 50
                }
                
                # Try multiple free endpoints
                endpoints = [
                    "https://text-summarizer-api.p.rapidapi.com/summarize",  # requires key
                    "https://api.meaningcloud.com/summarizer-1.0"  # requires key
                ]
                
                # Since free public APIs often need keys, let's use a different approach
                
                # Create a simple extractive summary (no API needed!)
                sentences = input_text.replace('\n', ' ').split('. ')
                word_count = len(input_text.split())
                
                # Simple algorithm: take first few sentences for summary
                if length == "Short":
                    num_sentences = 2
                elif length == "Medium":
                    num_sentences = 3
                else:
                    num_sentences = 5
                
                summary = '. '.join(sentences[:num_sentences]) + '.'
                
                st.success("✅ **Summary Ready!**")
                st.write(summary)
                
                # Show stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original", f"{len(input_text.split())} words")
                with col2:
                    st.metric("Summary", f"{len(summary.split())} words")
                
                st.info("💡 **Note:** Using basic summarization. For AI-powered results, we need a working API.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("📝 **Pro tip:** For better AI summaries, we can add a free API key from a working provider.")
