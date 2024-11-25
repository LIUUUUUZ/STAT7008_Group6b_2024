import streamlit as st
from utilities.chatbot import ChatBot
from utilities.mongodb import CloudData
from time import sleep
from utilities.XGBoost_Predictor import XGBoostPredictor
from utilities.data_processor import sub_grades_encoding
st.set_page_config(
    page_title="STAT7008B Group6b HomePage",
    page_icon="👋",
)

if "chat_bot_init" not in st.session_state:
    st.session_state.chat_bot_init = True
if "cd_init" not in st.session_state:
    st.session_state.cd = CloudData()
    st.session_state.cd_init = False
    st.session_state.cd_init = True
if "username" not in st.session_state:
    st.session_state.user_name = ""

if st.session_state.get("is_logged_in"):

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if st.session_state.chat_bot_init:
        api_key = st.session_state.cd.get_settings()['api_key']
        init_prompt = st.session_state.cd.get_settings()['init_prompt']
        st.session_state.chat_bot = ChatBot(api_key, init_prompt)
        st.session_state.risk_predictor = XGBoostPredictor()
        st.session_state.risk_predictor.load_model_and_stats("models/xgboost_model.json", "models/feature_medians.json")
        st.session_state.subgrade_encoder = sub_grades_encoding
        st.session_state.chat_bot_init = False
        st.session_state.messages.append({"role": "assistant", "content": "I am the credit risk ChatBot serving STAT7008B Group6b. How can I assist you?"})
        st.rerun()
    
    st.sidebar.success("Welcome, " + st.session_state["username"] + "!")
    st.sidebar.page_link(page="Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")
    if st.session_state.username == "admin":
        st.sidebar.page_link(page="pages/admin.py", label="Admin")

    st.header("🏢 Company Introduction")
    st.write("""
    Welcome to our company! We are a leading financial institution dedicated to providing comprehensive credit services to individuals and businesses. Our mission is to empower every client with the financial resources they need to achieve their goals. 

    In the context of today’s rapid development of financial technology, personal credit management has become increasingly complex and critical. Effective as- sessment of credit default risk is not only related to the stability and risk control ability of financial institutions, but also profoundly affects the credit history of borrowers and their future financing opportunities. Therefore, building an intelligent chatbot that collects user data in the form of a dialog box, analyzes individual credit default risk, and answers questions related to finance and credit will provide users with more informed credit decision support.
    """)



    with st.expander("📖 Learn More", expanded=True):
        st.write("Our analysis include:")
        st.write("- The data collection and cleaning module")
        st.write("- The personal finance credit problem analysis model")
        st.write("- The financial and credit knowledge data collection module")
        st.write("- The financial credit problem chat model")
        st.write("-  The UI interaction design module")
    # Additional contact information
    st.sidebar.header("📞 Contact Information")
    st.sidebar.write("Email: contact@connect.hku.hk")
    st.sidebar.write("Phone: +123 456 789")
    

else:
    st.header("🌲 STAT7008B Group6b")
    with st.container():
        c1, c2, c3 = st.tabs(["Login", "Register", "Forget Password"])
        with c1:
            st.warning("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.button("Login")
            if login:
                login_status, info = st.session_state.cd.user_login(username, password)
                if login_status:
                    st.session_state["is_logged_in"] = True
                    st.session_state["username"] = username
                    st.success(info)
                    sleep(1.5)
                    st.rerun()
                else:
                    st.error(info)
        with c2:
            st.warning("Register")
            username = st.text_input("Username", key="new_Username")
            password = st.text_input("Password", key="new_Password", type="password")
            email = st.text_input("Email")
            password_confirm = st.text_input("Confirm Password", type="password")
            register = st.button("Register")
            if register:
                if password != password_confirm:
                    reg_status, info = False, "Password and Confirm Password do not match"
                else:
                    reg_status, info = st.session_state.cd.add_user({"name":username, "email":email, "password":password})
                if reg_status:
                    st.success(info)
                    st.session_state["is_logged_in"] = True
                    st.session_state["username"] = username
                    sleep(1.5)
                    st.rerun()
                else:
                    st.error(info)

        with c3:
            st.warning("Forget Password")
            username = st.text_input("Username", key="forget_username")
            email = st.text_input("Email", key="forget_email")
            forget_password = st.button("Forget Password")
            if forget_password:
                status, info = st.session_state.cd.forget_password(username, email)
                if status:
                    st.success(info)
                else:
                    st.error(info)  
            