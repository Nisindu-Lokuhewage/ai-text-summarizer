import streamlit as st
from google import genai

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")
st.title("🤖 AI Text Summarizer")
st.markdown("Powered by **Google Gemini**")

# Get API key from Streamlit secrets (no user input needed)
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=200)

# Summary length
length = st.radio("📏 **Summary length**", 
                  options=["Short", "Medium", "Detailed"], index=0)

length_prompts = {
    "Short": "in 2-3 sentences",
    "Medium": "in 4-5 sentences",
    "Detailed": "in 6-8 sentences"
}

if st.button("✨ **Summarize**", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to summarize")
    else:
        with st.spinner("🤖 Thinking..."):
            try:
                # Using gemini-flash-latest - STABLE alias that always works [citation:4]
                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=f"Summarize the following text {length_prompts[length]}:\n\n{input_text}"
                )
                st.success("✅ **Summary**")
                st.write(response.text)
                
                # Word count metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original", f"{len(input_text.split())} words")
                with col2:
                    st.metric("Summary", f"{len(response.text.split())} words")
                    
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Get your free API key at [Google AI Studio](https://aistudio.google.com)")
