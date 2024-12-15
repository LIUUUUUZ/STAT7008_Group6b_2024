import streamlit as st
import streamlit.components.v1 as components

from st_chat_message import message

def clear_message():
    st.session_state.messages = []
    st.session_state.new_message = ""
    st.session_state.chat_bot.reset()

def clear_text():
    st.session_state.new_message = st.session_state["chat_input"]
    st.session_state.new_input = st.session_state["chat_input"]
    st.session_state["chat_input"] = ""

st.set_page_config(
    page_title="STAT7008B Group6b ChatBot",
    page_icon="👋",
    layout="wide",
)

# Initialize user session if not set

if "new_message" not in st.session_state:
    st.session_state.new_message = ""

if "new_input" not in st.session_state:
    st.session_state.new_input = ""

if st.session_state.get("is_logged_in"):

    st.sidebar.success("Welcome, " + st.session_state["username"] + "!")
    st.sidebar.page_link(page="./Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")
    if st.session_state.username == "admin":
        st.sidebar.page_link(page="pages/admin.py", label="Admin")
    # Page title
    with st.container():
        c1, c2 = st.columns([4,1])
        with c1:
            st.write("## 🤖 💬 ChatBot")
        with c2:
            st.markdown(
            """
            <div style="position: relative; height: 100%;">
            </div>
            """,
            unsafe_allow_html=True,
            )
            if len(st.session_state.messages) > 1:
                st.button("Clear Chat", key="clear_button", on_click=clear_message)

    with st.container(height=550, border=True, key="chat-container"):
        for m in st.session_state.messages:
            if m['role'] == 'user':
                message(m['content'], is_user=True)
            else:
                message(m['content'])

    if st.session_state.new_input:
        st.session_state.messages.append({"role": "user", "content": st.session_state.new_message})
        st.session_state.new_input = ""
        st.rerun()
    if st.session_state.new_message:
        bot_reply = st.session_state.chat_bot(st.session_state.new_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.session_state.new_message = ""
        st.rerun()
    st.text_input(label="user_input",placeholder="Type your message here...", key="chat_input", value="", label_visibility="collapsed", max_chars=200, on_change=clear_text)
    
else:
    st.switch_page("./Homepage.py")