# STAT7008_Group6b_2024
### 2024 第二学期 STAT7008B 的小组期末项目 组员(连子清，刘知闲(组长)，田潇文，张哲)(按拼音排序)
1.后续的项目规划和分工会写在此readme file中.
2.各位更新的话记得同步更新此readme file且在commit changes时写好comment便于其他组员查看进度。
3.如果有问题以及建议请及时在微信群中反馈。

### 目前项目为: Project 6 Loan Enquiry and Credit Risk Analysis Chatbot (Banking and Finance for __INDIVIDUALS__) 

### 目标为: __设计一个可以以对话框形式收集数据分析个人信贷违约风险及提供部分有关金融信贷问题问答的网络聊天机器人__

### 项目模块分为:
1. 数据收集与清洗模块
2. 个人金融信贷问题分析模型的构建模块(catboost)
3. 金融信贷知识数据收集模块
4. 金融信贷问题聊天模型的构建模块
5. UI模块与各模块的整合

### 准备使用的模型数据为:
1. [https://www.kaggle.com/code/mathchi/credit-risk-evaluation](https://www.kaggle.com/code/mathchi/credit-risk-evaluation)
2. [https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset](https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset) <font color=green/> √ <font>
3. [https://www.kaggle.com/datasets/laotse/credit-risk-dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)


### 1.数据收集与清洗模块：     
1. 数据收集以及初步筛选：田潇文，刘知闲 10.23-10.25 （已完成）
   经过初步分析最终选取[https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset](https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset) 数据集作为信用风险模型的训练集。      
   数据整理及分析由田潇文及刘知闲共同完成，过程详情保存在data_analysis.ipynb中。     
2. 数据分析及筛选(清洗)：张哲, 刘知闲 10.26之前-10.31 （已完成）   
   其中核心筛选catboost模块由张哲负责，数据清洗以及encoder由刘知闲负责。     
   目前此项目核心分析模型将使用由catboost选取的前15个最相关的特征进行训练， 同时使用随机选取的15个特征作为对照。     
3. 代码模块化：刘知闲，张哲：10.23-10.31 （部分完成）
   此过程模块为DataLoader模块， 详细请见utilities中的data_processor.py      

### 2.模型的训练与ui模块搭建
1. 信贷风险模型训练以及后续使用方式的设计：张哲
2. 相关金融信贷风险知识问答语言模型的设计/运用：田潇文
3. 此项目UI及chatbot搭建等交互设计：刘知闲， 连子清
         

### 运行project： 在项目文件里运行 streamlit run Homepage.py

### [https://youtu.be/XaFjIcuxv0A](Demo Video)
