import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage

# ChatBot class definition
class ChatBot():
    def __init__(self, api_key: str = "", init_prompt: str = ""):
        self.chat = ChatOpenAI(
            openai_api_base="https://chatapi.littlewheat.com/v1", 
            openai_api_key=api_key
        )
        self.init_prompt: str = init_prompt
        self.messages = [SystemMessage(content=self.init_prompt)]

    def _send_message(self, human_input: str) -> str:
        self.messages.append({"role": "user", "content": human_input})
        response = self.chat(self.messages)
        self.messages.append({"role": "assistant", "content": response.content})
        return response.content

    def __call__(self, human_input: str) -> str:
        return self._send_message(human_input)

# Setting page title
st.set_page_config(page_title="Chat AI", layout="wide")

# Initialize user session if not set
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = "https://via.placeholder.com/50"
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Page title
st.title("📚 STAT 7008 Group Work")
st.header("🤖 💬 Chat AI")

# Sidebar section
if st.session_state.logged_in:
    st.sidebar.header(f"👋 Welcome, {st.session_state.username}")
    st.sidebar.image(st.session_state.user_avatar, width=50)
    st.sidebar.write("✅ You are currently logged in.")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_avatar = "https://via.placeholder.com/50"
        st.session_state.messages = []
        st.experimental_rerun()
else:
    st.sidebar.write("🔒 You are not logged in.")

# Scrollable chat area for displaying messages
st.markdown("""
    <div style="height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; background-color: #f8f8f8;">
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"👤 {message['content']}")
    else:
        st.write(f"🤖 {message['content']}")

st.markdown("</div>", unsafe_allow_html=True)

# Input section fixed at the bottom
st.markdown("""
    <style>
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 10px;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

# Create input field and buttons
with st.container():
    user_input = st.text_input("Type your message here...", key="chat_input", value="", label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Send", key="send_button"):
            if user_input:
                chatbot = ChatBot(api_key="YOUR_API_KEY", init_prompt="You are a helpful assistant.")
                try:
                    bot_reply = chatbot(user_input)
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    st.experimental_rerun()
                except Exception as e:
                    st.error("🔴 Error: Unable to get response from AI. Please try again.")

    with col2:
        if st.button("🗑️ Clear Messages", key="clear_button"):
            st.session_state.messages = []  # Clear chat history
            st.experimental_rerun()

# Custom CSS to fix the input section at the bottom
st.markdown("""
    <style>
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 10px;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("is_logged_in"):
    st.sidebar.page_link(page="./Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")

    st.sidebar.title("可在sidebar中添加所需部分")

else:
    st.switch_page("./Homepage.py")