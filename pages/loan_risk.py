import streamlit as st

sub_grades = ["A1","A2","A3","A4","A5","B1","B2","B3","B4","B5","C1","C2","C3","C4","C5","D1","D2","D3","D4","D5","E1","E2","E3","E4","E5","F1","F2","F3","F4","F5","G1","G2","G3","G4","G5",None]

if st.session_state.get("is_logged_in"):

    st.sidebar.success("Welcome, " + st.session_state["username"] + "!")
    st.sidebar.page_link(page="./Homepage.py", label="Homepage")
    st.sidebar.page_link(page="pages/chatbot.py", label="Chatbot")
    st.sidebar.page_link(page="pages/news.py", label="News")
    st.sidebar.page_link(page="pages/loan_risk.py", label="Loan Risk Prediction")
    if st.session_state.username == "admin":
        st.sidebar.page_link(page="pages/admin.py", label="Admin")
    with st.container():
        st.header("Loan Risk Prediction")
        st.write("""Please write your true infomation here, you can leave the blank if you don't have the infomation.
                    The more precise the information, the more accurate the prediction will be.""")
        with st.form(key="loan_risk_form"):
            funded_amnt = st.number_input("Funded Amnt/贷款金额", value=None, step=1)
            tot_cur_bal = st.number_input("Tot Cur Bal/账户总资产", value=None, step=1)
            int_rate = st.number_input("Int Rate/借款利率 %", value=None)
            sub_grade = st.selectbox("Sub Grade/您的信用等级", sub_grades,index=35)
            annual_inc = st.number_input("Annual Inc/ 年收入", value=None, step=1)
            out_prncp = st.number_input("Out Prncp/未偿还本金", value=None, step=1)
            last_pymnt_amnt = st.number_input("Last Pymnt Amnt/最近偿还的金额", value=None, step=1, min_value=0)
            recoveries = st.number_input("Recoveries/已偿还的本金及利息", value=None, step=1, min_value=0)
            inq_last_6mths = st.number_input("Inq for credit Last 6mths/ 最近6个月的查询信用次数", value=None, step=1, min_value=0)
            total_rev_hi_lim = st.number_input("Total Rev Hi Lim/ 高信用发放额度总和", value=None, step=1, min_value=0)
            collections_12_mths_ex_med = st.number_input("Collections 12 Mths Ex Med/除医疗账单过去12个月被催收次数", value=None, step=1, min_value=0)
            delinq_2yrs = st.number_input("Delinq 2yrs/过去2年逾期次数", value=None, step=1, min_value=0)
            dti = st.number_input("Dti/债务收入比", value=None, min_value=0.00, step=0.01)
            pub_rec = st.number_input("Pub Rec/不良公共记录次数", value=None, step=1, min_value=0)
            acc_now_delinq = st.number_input("Acc Now Delinq/当前逾期账户总量", value=None, step=1, min_value=0)
            tot_coll_amt = st.number_input("Tot Coll Amt/曾经欠下的总催收金额", value=None, step=1, min_value=0)
            submit = st.form_submit_button("Submit")
            if submit:
                input_data = {}
                if out_prncp is not None:
                    input_data["out_prncp"] = out_prncp
                if last_pymnt_amnt is not None:
                    input_data["last_pymnt_amnt"] = last_pymnt_amnt
                if tot_cur_bal is not None:
                    input_data["tot_cur_bal"] = tot_cur_bal
                if recoveries is not None:
                    input_data["recoveries"] = recoveries
                if int_rate is not None:
                    input_data["int_rate"] = int_rate
                if inq_last_6mths is not None:
                    input_data["inq_last_6mths"] = inq_last_6mths
                if sub_grade is not None:
                    input_data["sub_grade"] = st.session_state.subgrade_encoder(sub_grade)
                if total_rev_hi_lim is not None:
                    input_data["total_rev_hi_lim"] = total_rev_hi_lim
                if annual_inc is not None:
                    input_data["annual_inc"] = annual_inc
                if collections_12_mths_ex_med is not None:
                    input_data["collections_12_mths_ex_med"] = collections_12_mths_ex_med
                if delinq_2yrs is not None:
                    input_data["delinq_2yrs"] = delinq_2yrs
                if dti is not None:
                    input_data["dti"] = dti
                if funded_amnt is not None:
                    input_data["funded_amnt"] = funded_amnt
                if pub_rec is not None:
                    input_data["pub_rec"] = pub_rec
                if acc_now_delinq is not None:
                    input_data["acc_now_delinq"] = acc_now_delinq
                if tot_coll_amt is not None:
                    input_data["tot_coll_amt"] = tot_coll_amt

                result = st.session_state.risk_predictor.predict(input_data)
                prompt = f"The costumer's loan risk is {result}, the higher the risk, the more likely the customer will default. The original potential loan amount is {funded_amnt}. If the risk is good credit you can answer the high success rate of this loan, if the risk is bad credit you can answer the low success rate and under consideration. Use second person view to answer the question."
                st.session_state.messages = []
                st.session_state.new_message = ""
                st.session_state.chat_bot.reset()
                bot_reply = st.session_state.chat_bot(prompt)
                bot_reply += f" The Pridiction Result is only for reference, the final decision should be made by the bank. If you have any question, please ask me."
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.switch_page("pages/chatbot.py")
                
            
else:
    st.switch_page("./Homepage.py")