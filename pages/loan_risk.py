import streamlit as st

if st.session_state.get("is_logged_in"):

    st.sidebar.page_link(page="./Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")

    st.sidebar.title("可在sidebar中添加所需部分")

else:
    st.switch_page("./Homepage.py")