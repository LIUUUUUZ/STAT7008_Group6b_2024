import streamlit as st
from utilities.chatbot import ChatBot
from utilities.mongodb import CloudData

st.set_page_config(
    page_title="STAT7008B Group6b HomePage",
    page_icon="👋",
)

if "chat_bot_init" not in st.session_state:
    st.session_state.chat_bot_init = True


if st.session_state.get("is_logged_in"):

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if st.session_state.chat_bot_init:
        cd = CloudData()
        api_key = cd.get_settings()['api_key']
        init_prompt = cd.get_settings()['init_prompt']
        st.session_state.chat_bot = ChatBot(api_key, init_prompt)
        st.session_state.chat_bot_init = False
        st.session_state.messages.append({"role": "assistant", "content": "I am the credit risk ChatBot serving STAT7008B Group6b. How can I assist you?"})
        st.rerun()
    
    st.sidebar.page_link(page="Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")
    
    st.write("Welcome to the ChatBot of STAT7008B Group6b! 👋")

    st.markdown(
        """
        这是已经登陆的页面
        """
        )
    st.sidebar.success("这里是登陆后的页面")
    

else:
    login_button = st.button("Log in")
    if login_button:    
        st.session_state["is_logged_in"] = True
        # refresh the page
        st.rerun()

    st.write("# Welcome to Streamlit! 👋")

    st.error("这是没有登陆的页面")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
            Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )