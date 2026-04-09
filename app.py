import streamlit as st
import google.generativeai as genai
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Chat Assistant", page_icon="🌙", layout="wide")

# 2. Advanced Dark Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #1a1c24 100%);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* Chat Message Boxes */
    [data-testid="stChatMessage"] {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        color: #ffffff !important; /* Forces text to white */
    }

    /* Ensure text inside chat is readable */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
        color: #e6edf3 !important;
    }

    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }

    /* Titles and Text */
    h1, h2, h3, span, p {
        color: #ffffff !important;
    }

    /* Clear Button */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #238636;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("⚙️ Controls")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.success("Mode: Dark Stealth")

# 4. API Logic
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

@st.cache_data(show_spinner=False)
def get_response(user_query, _model):
    try:
        return _model.generate_content(user_query).text
    except Exception as e:
        if "429" in str(e): return "Rate limit hit. Please wait a moment."
        return f"Error: {e}"

# 5. Main Interface
st.title("🌙 Stealth AI Assistant")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing..."):
                response_text = get_response(prompt, model)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
else:
    st.warning("Please enter your API Key in the sidebar.")
