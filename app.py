import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")
st.markdown("Enter your API key and text to get a smart summary")

# API Key input
api_key = st.text_input("🔑 **Google Gemini API Key**", type="password", help="Get your key from https://aistudio.google.com")

# Text input
input_text = st.text_area("📄 **Text to summarize**", height=150, placeholder="Paste or type your text here...")

# Summary length option
length = st.select_slider("📏 **Summary length**", options=["Very Short", "Short", "Medium"], value="Short")

# Map length to instruction
length_map = {
    "Very Short": "one sentence",
    "Short": "two to three sentences", 
    "Medium": "four to five sentences"
}

# Summarize button
if st.button("✨ **Summarize**", type="primary"):
    if not api_key:
        st.error("❌ Please enter your Gemini API key")
    elif not input_text.strip():
        st.warning("⚠️ Please enter some text to summarize")
    else:
        try:
            with st.spinner("🤖 Summarizing..."):
                # Configure Gemini
                genai.configure(api_key=api_key)
                
                # TRY THIS MODEL NAME - 'gemini-pro' works most reliably
                model = genai.GenerativeModel('gemini-pro')
                
                # Create prompt
                prompt = f"""Summarize the following text in {length_map[length]}. Keep the key information and main points.

Text: {input_text}

Summary:"""
                
                # Generate response
                response = model.generate_content(prompt)
                
                # Display result
                st.success("✅ **Summary**")
                st.write(response.text)
                
                # Show stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original", f"{len(input_text.split())} words")
                with col2:
                    st.metric("Summary", f"{len(response.text.split())} words")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("💡 Make sure your API key is valid and you have Gemini API access enabled")

# Footer
st.markdown("---")
st.markdown("Powered by **Google Gemini AI**")
