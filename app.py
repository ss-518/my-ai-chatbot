import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Pro AI Assistant", page_icon="🌓", layout="wide")

# 2. Initialize Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# 3. Define Theme Variables
if st.session_state.theme == "dark":
    bg_color = "#0e1117"
    text_color = "#ffffff"
    msg_bg = "#21262d"
    sidebar_bg = "#161b22"
    border_color = "#30363d"
    input_bg = "#0d1117"
    mode_label = "Dark"
else:
    bg_color = "#ffffff"
    text_color = "#1f1f1f"
    msg_bg = "#f6f8fa"
    sidebar_bg = "#f6f8fa"
    border_color = "#d0d7de"
    input_bg = "#ffffff"
    mode_label = "Light"

# 4. Injected CSS (Aggressive color forcing)
st.markdown(f"""
    <style>
    /* Global Background and Text */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* Chat Bubbles */
    [data-testid="stChatMessage"] {{
        background-color: {msg_bg} !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
    }}

    /* Input Box (The "Search" Section) */
    .stChatInputContainer textarea {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {msg_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        width: 100%;
    }}

    /* Force all headings and paragraphs */
    h1, h2, h3, p, li, span {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    # Toggle Button
    if st.button(f"Mode: {mode_label}"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 6. API Logic
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter API Key", type="password")

@st.cache_data(show_spinner=False)
def get_response(user_query, _model):
    try:
        return _model.generate_content(user_query).text
    except Exception as e:
        return f"Error: {e}"

# 7. Main UI
st.title("🌓 AI Assistant")

if api_key:
    genai.configure(api_key=api_key)
    # Using Flash-Lite for better quota management
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you today?"):
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
