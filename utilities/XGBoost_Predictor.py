import xgboost as xgb
import pandas as pd
import os
import json


class XGBoostPredictor:
    def __init__(self, model: xgb.Booster = None):
        self.model = model
        self.feature_names = None  # 用于存储模型的特征名
        self.feature_medians = None  # 用于存储训练数据的特征中位数

    def load_model_and_stats(self, model_path: str, stats_path: str) -> None:
        # 加载模型
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}.")
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        # 加载特征中位数
        if not os.path.exists(stats_path):
            raise FileNotFoundError(f"Feature statistics file not found at {stats_path}.")
        with open(stats_path, "r") as f:
            self.feature_medians = json.load(f)
        self.feature_names = list(self.feature_medians.keys())

    def format_input(self, input_data: dict) -> pd.DataFrame:
        if self.feature_medians is None or self.feature_names is None:
            raise ValueError("Feature statistics are not set. Please call load_model_and_stats() first.")

        # 将输入数据转换为 DataFrame
        user_input = pd.DataFrame([input_data])

        # 补全缺失特征
        for feature in self.feature_names:
            if feature not in user_input.columns:
                user_input[feature] = self.feature_medians[feature]

        # 按训练时的特征顺序对齐
        user_input = user_input[self.feature_names]

        return user_input

    def predict(self, input_data: dict) -> str:
        if self.model is None:
            raise ValueError("Model is not loaded. Please load a model first.")

        # 格式化输入数据
        user_input = self.format_input(input_data)

        # 转换为 DMatrix 格式
        dmatrix = xgb.DMatrix(user_input)

        # 进行预测
        predictions = self.model.predict(dmatrix)

        # 定义映射关系
        risk_mapping = {
            0: "Good credit",
            1: "Good credit",
            4: "Good credit",
            5: "Good credit",
            7: "Good credit",
            3: "Medium risk",
            6: "Medium risk",
            2: "High risk",
            9: "High risk"
        }

        # 获取预测值
        predicted_class = int(predictions[0])

        # 映射到对应的风险等级
        risk_level = risk_mapping.get(predicted_class, "Unknown risk")

        return risk_level
