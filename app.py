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

length_map = {
    "Very Short": "one sentence",
    "Short": "two to three sentences", 
    "Medium": "four to five sentences"
}

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
                
                # ⭐ KEY FIX: Use the v1 client instead of v1beta
                import google.ai.generativelanguage as glm
                client = glm.GenerativeServiceClient(
                    client_options={"api_endpoint": "generativelanguage.googleapis.com:443"},
                    transport="rest"
                )
                
                # Use gemini-1.5-flash (free tier works)
                model_name = "models/gemini-1.5-flash"
                
                # Create the prompt
                prompt = f"Summarize the following text in {length_map[length]}. Keep the key information.\n\nText: {input_text}\n\nSummary:"
                
                # Make the request using v1
                from google.ai.generativelanguage import GenerateContentRequest, Content, Part
                
                request = GenerateContentRequest(
                    model=model_name,
                    contents=[Content(parts=[Part(text=prompt)])]
                )
                
                response = client.generate_content(request)
                
                # Display result
                st.success("✅ **Summary**")
                st.write(response.candidates[0].content.parts[0].text)
                
                # Show stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original", f"{len(input_text.split())} words")
                with col2:
                    st.metric("Summary", f"{len(response.candidates[0].content.parts[0].text.split())} words")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("💡 Make sure your API key is valid")

st.markdown("---")
st.markdown("Powered by **Google Gemini 1.5 Flash**")
