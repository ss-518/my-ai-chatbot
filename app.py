import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Pro AI Assistant", page_icon="🌓", layout="wide")

# 2. Initialize Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # Default to dark

# 3. Define CSS for both themes
if st.session_state.theme == "dark":
    bg_color = "#0e1117"
    text_color = "#ffffff"
    msg_bg = "#21262d"
    sidebar_bg = "#161b22"
    border_color = "#30363d"
    mode_label = "Dark"
else:
    bg_color = "#f0f2f6"
    text_color = "#1f1f1f"
    msg_bg = "#ffffff"
    sidebar_bg = "#ffffff"
    border_color = "#d1d5db"
    mode_label = "Light"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color};
    }}
    [data-testid="stChatMessage"] {{
        background-color: {msg_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 15px !important;
        color: {text_color} !important;
    }}
    h1, h2, h3, p, span, li {{
        color: {text_color} !important;
    }}
    /* Style the input text color based on theme */
    .stChatInput textarea {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar with Theme Toggle
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Theme Toggle Button
    if st.button(f"Mode: {mode_label}"):
        if st.session_state.theme == "dark":
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 5. API Logic
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

@st.cache_data(show_spinner=False)
def get_response(user_query, _model):
    try:
        return _model.generate_content(user_query).text
    except Exception as e:
        return f"Error: {e}"

# 6. Main Chat Interface
st.title("🌓 Pro AI Assistant")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
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
