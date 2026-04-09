import streamlit as st
import google.generativeai as genai
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Chat Assistant", page_icon="✨", layout="wide")

# 2. Inject Custom CSS for a Professional Look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
    }
    .stSidebar {
        background-color: rgba(255, 255, 255, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Controls
with st.sidebar:
    st.title("🤖 Bot Settings")
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.info("Powered by Gemini 2.5 Flash-Lite")

# 4. API Logic
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# --- Caching & Response Logic ---
@st.cache_data(show_spinner=False)
def get_response(user_query, _model):
    try:
        return _model.generate_content(user_query).text
    except Exception as e:
        return f"Error: {e}"

# 5. Main Chat Interface
st.title("Pro AI Assistant")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        # Using avatars to make it visual
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response_text = get_response(prompt, model)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
else:
    st.warning("Please configure your API Key in the sidebar.")
