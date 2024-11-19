import xgboost as xgb
from sklearn.metrics import accuracy_score
import pandas as pd

def train_and_evaluate_xgboost(x_train, x_test, y_train, y_test):
    # 将数据转换为 DMatrix 格式，启用分类特征支持
    dtrain = xgb.DMatrix(x_train, label=y_train)
    dtest = xgb.DMatrix(x_test, label=y_test)

    # 设置参数
    params = {
        'objective': 'multi:softmax',
        'eval_metric': 'mlogloss',
        'num_class': 10,
        'max_depth': 6,
        'eta': 0.3,
        'gamma': 0,
        'subsample': 1,
        'colsample_bytree': 1
    }

    # 训练模型
    num_rounds = 200
    bst = xgb.train(params, dtrain, num_boost_round=num_rounds, evals=[(dtest, 'test')])

    # 预测
    preds = bst.predict(dtest)

    # 评估
    accuracy = accuracy_score(y_test, preds)
    print(f"Accuracy: {accuracy}")

    return bst, accuracy
