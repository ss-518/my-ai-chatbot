import streamlit as st
import google.generativeai as genai

# 1. Setup the Page Layout
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("AI Chatbot")
st.caption("A school project powered by Gemini 1.5 Flash")

# 2. --- SECRETS & API CONFIGURATION ---
# This checks if the key is in Streamlit "Secrets". 
# If not (like when you run it locally), it shows a sidebar input.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # 3. --- CHAT HISTORY LOGIC ---
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. --- CHAT INPUT & RESPONSE ---
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response from Gemini
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please add the 'GEMINI_API_KEY' to Streamlit Secrets to activate the bot.")
