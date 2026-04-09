import streamlit as st
import google.generativeai as genai
import time

# 1. Setup the Page Layout
st.set_page_config(page_title="Upgraded AI Chatbot", page_icon="🚀")
st.title("Pro AI Chatbot")
st.caption("Now with High-Throughput (Gemini 2.5 Flash-Lite) & Smart Caching")

# 2. --- SECRETS & API CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 3. --- SMART CACHING FUNCTION ---
# This saves answers to common questions to save your API quota
@st.cache_data(show_spinner="AI is thinking...", ttl=3600)  # Caches for 1 hour
def get_ai_response(user_query, _model_instance):
    max_retries = 3
    retry_delay = 5  # Seconds to wait between retries
    
    for attempt in range(max_retries):
        try:
            response = _model_instance.generate_content(user_query)
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                st.warning(f"Rate limit hit. Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff (5s, then 10s)
            else:
                return f"Error: {e}"

# 4. --- INITIALIZE CHAT ---
if api_key:
    genai.configure(api_key=api_key)
    # Using the 2.5 Flash-Lite model for maximum free-tier requests
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. --- CHAT INPUT ---
    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Use the cached function to get the response
        full_response = get_ai_response(prompt, model)
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("Please add your API Key to start.")
