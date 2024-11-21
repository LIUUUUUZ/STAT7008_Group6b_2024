import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
try: import gdown 
except ImportError: print('Please install gdown by running: pip install gdown')
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from joblib import load
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def sub_grades_encoding(x: str) -> float:
        val = 0
        if 'A' in x:
            val = 7
        elif 'B' in x:
            val = 6
        elif 'C' in x:
            val = 5
        elif 'D' in x:
            val = 4
        elif 'E' in x:
            val = 3
        elif 'F' in x:
            val = 2
        elif 'G' in x:
            val = 1
        if '1' in x:
            val += 0.8
        elif '2' in x:
            val += 0.6
        elif '3' in x:
            val += 0.4
        elif '4' in x:
            val += 0.2
        elif '5' in x:
            val += 0.0
        return val



def verification_status(x: str) -> int:

    if x == 'Not Verified':

        return 0

    return 1


def loan_status(x: str) -> int:
    if x == 'Current':
        return 0
    elif x == 'Fully Paid':
        return 1
    elif x == 'Charged Off':
        return 2
    elif x == 'Late (31-120 days)':
        return 3
    elif x == 'Issued':
        return 4
    elif x == 'In Grace Period':
        return 5
    elif x == 'Late (16-30 days)':
        return 6
    elif x == 'Does not meet the credit policy. Status:Fully Paid':
        return 7
    elif x == 'Default':
        return 8
    elif x == 'Does not meet the credit policy. Status:Charged Off':
        return 9
    else:
        raise ValueError('Unknown loan status: ' + x)
    
def maxmin_scaler(x: pd.DataFrame) -> pd.DataFrame:
    scaler: MinMaxScaler = load('models/scaler.joblib')
    cols: pd.DataFrame = x.columns
    x = scaler.transform(x)
    x: pd.DataFrame = pd.DataFrame(x, columns=cols)
    return x
    


class DataPreProcessor():
    def __init__(self, input_name: str = 'data.csv', output_name: str = 'cleaned_data.csv', data_folder: str = '../dataset') -> None:
        self.data: pd.DataFrame = pd.DataFrame()
        self.loaded: bool = False
        assert input_name != output_name, 'input_name and output_name should not be the same'
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        if data_folder[-1] != '/':
            data_folder += '/'
        if not input_name.endswith('.csv'):
            input_name += '.csv'
        if not output_name.endswith('.csv'):
            output_name += '.csv'
        self.data_folder: str = data_folder
        self.input_path: str = data_folder + input_name
        self.output_path: str = data_folder + output_name
        self.filled: bool = False

    def show_data_info(self, n: int = 5, only_head: bool = False, only_shape: bool = False) -> None:
        if not self.loaded:
            print('Data not loaded, please load the data first')
            return
        # print the shape of the data
        print(f'processed: {self.processed}')
        if only_shape:
            print(f'data shape: {self.data.shape}')
            return
        elif only_head:
            print(f'data head: \n {self.data.head(n)}')
            return
        print(f'data shape: {self.data.shape}')
        self.data.info()
        print(f'data head: \n {self.data.head(n)}')
        return

    def load_data(self, download: bool = False) -> None:
        if not os.path.exists(self.input_path) and not download:
            print('File does not exist, be sure to turn on download or check the input path, current path is: ', self.input_path)
            return
        elif not os.path.exists(self.input_path) and download:
            url: str = 'https://drive.google.com/uc?id=1DgyuTGhIlQ4nwHBkXhwk5FAoCSgR_acZ'
            gdown.download(url, self.input_path, quiet=False)
        
        self.data: pd.DataFrame = pd.read_csv(self.input_path, index_col=0)
        self.loaded: bool = True
        self.processed: bool = False
        return 
    
    def get_data(self) -> pd.DataFrame:
        if not self.loaded:
            print('Data not loaded, please load the data first')
            return
        return self.data

    def preprocess_data(self, drop_JOINT: bool = True, 
                        dropna_percent: int = 20, 
                        drop_policy_code: bool = True, 
                        drop_by_analysis: bool = True, 
                        drop_insignificant_missing_value: bool = True, 
                        fill_blank: bool = True,
                        fill_mode: str = 'mode',
                        ) -> None:
        row_deleted: list = []
        row_delete_reason: list = []
        col_deleted: list = []
        col_delete_reason: list = []
        if drop_JOINT:
            row_before: int = self.data.shape[0]
            self.data: pd.DataFrame = self.data[self.data['application_type'] != 'JOINT']
            row_deleted.append(row_before - self.data.shape[0])
            row_delete_reason.append('del application_type \'JOINT\'')
            col_before: int = self.data.shape[1]
            columns_to_drop: list = [i for i in self.data.columns if 'joint' in i]
            columns_to_drop.append('application_type')
            self.data.drop(columns=columns_to_drop, inplace=True)
            col_deleted.append(col_before - self.data.shape[1])
            col_delete_reason.append('del columns related to \'joint\', namely: ' + ', '.join(columns_to_drop))

        if dropna_percent > 0:
            columns_to_drop = []
            for i in self.data.columns:
                if self.data[i].isna().mean()*100 > dropna_percent:
                    columns_to_drop.append(i)
            self.data.drop(columns=columns_to_drop, inplace=True)
            col_deleted.append(len(columns_to_drop))
            col_delete_reason.append(f'del columns with more than {dropna_percent}% missing values, namely: ' + ', '.join(columns_to_drop))
        
        if drop_policy_code:

            columns_to_drop = ['policy_code']
            self.data.drop(columns=columns_to_drop, inplace=True)
            col_deleted.append(len(columns_to_drop))
            col_delete_reason.append('del columns \'policy_code\'')
        
        if drop_by_analysis:
            columns_to_drop = ['member_id', 'url', 'issue_d', 'earliest_cr_line', 'grade', 'last_credit_pull_d','emp_title', 'title', 'zip_code', 'addr_state', 'last_pymnt_d', 'pymnt_plan', 'emp_length']
            self.data.drop(columns=columns_to_drop, inplace=True)
            col_deleted.append(len(columns_to_drop))
            col_delete_reason.append('del columns after analyzing (analyzing procedures are in the file \'data_analysis.ipynb\'), namely: ' + ', '.join(columns_to_drop))
        
        if drop_insignificant_missing_value:
            na_percentages = self.data.isna().mean() * 100
            na_percentages = na_percentages[na_percentages > 0]
            row_before: int = self.data.shape[0]
            for i in na_percentages.index:
                if na_percentages[i] < 1:
                    self.data.dropna(subset=[i], inplace=True)

            row_deleted.append(row_before - self.data.shape[0])
            row_delete_reason.append('del rows with insignificant missing values')

        if fill_blank:
            blank_columns: list = self.data.columns[self.data.isna().any()].tolist()

            assert fill_mode in ['mean', 'mode', 'zero', 'remove'], 'mode should be either mean, mode, zero or remove'
            if fill_mode == 'mean':
                for i in blank_columns:
                    self.data[i].fillna(self.data[i].mean(), inplace=True)

            elif fill_mode == 'mode':
                for i in blank_columns:
                    self.data[i].fillna(self.data[i].mode()[0], inplace=True)
            
            elif fill_mode == 'zero':
                for i in blank_columns:
                    self.data[i].fillna(0, inplace=True)

            elif fill_mode == 'remove':
                self.data.dropna(subset=blank_columns, inplace=True)

            assert self.data.isna().sum().sum() == 0, 'ERROR, There are still blank values in the data'
            self.filled: bool = True

        print('Data Preprocessing Summary:')
        print(f'Rows Deleted: {sum(row_deleted)}')
        for i in range(len(row_deleted)):
            print(f'\t{row_deleted[i]} rows deleted due to {row_delete_reason[i]}')
        print(f'Columns Deleted: {sum(col_deleted)}')
        for i in range(len(col_deleted)):
            print(f'\t{col_deleted[i]} columns deleted due to {col_delete_reason[i]}')
        if fill_blank:
            print(f'Blank values filled with {fill_mode}, relative columns: {blank_columns}')
        self.processed: bool = True
        return
    
    def show_feature_plt(self) -> None:
        # plot all the features, n unique > 2
        features = [col for col in self.data.columns if self.data[col].nunique() > 2]
        rows = (len(features) + 2) // 4
        cols = 4
        # Set up the figure and axis for subplots
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
        axes = axes.flatten()  # Flatten in case of multiple rows
        fig.patch.set_facecolor('lightgray')  # Set the background color of the entire figure
        palette = sns.color_palette('Set2', len(features))
        plotted_df = self.data.copy()
        plotted_df['diff_loan_funded'] = plotted_df['loan_amnt'] - plotted_df['funded_amnt']
        for i, col in enumerate(features):
            sns.histplot(x=plotted_df[col], kde=False, ax=axes[i], color=palette[i], alpha=1)  # Set alpha slightly transparent for better visualization
            axes[i].set_title(col)
        # Remove any empty subplots (in case the number of features doesn't fill the grid)
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        fig.suptitle("Distributions of Features", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for the main title
        plt.show()
        return
    



class DataLoader():
    def __init__(self, data: pd.DataFrame, mode: str = "random") -> None:
        self.data: pd.DataFrame = data
        self.mode: str = mode
        self.encodered: bool = False
        self.splited: bool = False
        self.filtered: bool = False
        self.filled: bool = True

    def encoder(self) -> None:
        if self.encodered:
            print('Data already encoded')
            return

        # 公共编码
        self.data['sub_grade'] = self.data['sub_grade'].apply(sub_grades_encoding)
        self.data['verification_status'] = self.data['verification_status'].apply(verification_status)
        label_encoder = LabelEncoder()
        self.data['term'] = label_encoder.fit_transform(self.data['term'])
        self.data['initial_list_status'] = label_encoder.fit_transform(self.data['initial_list_status'])

        if self.mode == "random":
            # 独热编码
            categorical_features = self.data.select_dtypes(include='object').drop(columns=['loan_status'])
            encoded_features: pd.DataFrame = pd.get_dummies(categorical_features, dtype=int)
            self.data = pd.concat([self.data, encoded_features], axis=1)
            self.data.drop(columns=categorical_features.columns, inplace=True)
        elif self.mode =="catboost":
            # 保留原始分类特征
            pass

        self.data['loan_status'] = self.data['loan_status'].apply(loan_status)
        self.encodered: bool = True

    def split_data(self, dataset_size = 0.1, test_size: float = 0.3, random: bool = True, MAXMIN: bool = True) -> tuple:
        if self.splited:
            print('Data already splited')
            return
        if not self.encodered and not self.filled:
            print('Data not encoded or filled, please encode and fill the data first')
            return
        x: pd.DataFrame = self.data.drop(columns=['loan_status'])
        y: pd.DataFrame = self.data['loan_status']
        x_rest, self.X, y_rest, self.Y = train_test_split(x, y, test_size=dataset_size, random_state=1 if random else None)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=test_size, random_state=1 if random else None, stratify=self.Y, shuffle=True)
        self.splited: bool = True

        if self.mode == "random" and MAXMIN:
            # 默认归一化
            self.x_train = maxmin_scaler(self.x_train)
            self.x_test = maxmin_scaler(self.x_test)
        
        elif self.mode == "catboost":
            # CatBoost模式处理分类特征为字符串
            categorical_cols = self.x_train.select_dtypes(exclude=[np.number]).columns
            for col in categorical_cols:
                self.x_train[col] = self.x_train[col].astype(str)
                self.x_test[col] = self.x_test[col].astype(str)

            # 对数值型特征进行归一化
            numeric_features = self.x_train.select_dtypes(include=[np.number]).columns
            scaler = MinMaxScaler()
            self.x_train[numeric_features] = scaler.fit_transform(self.x_train[numeric_features])
            self.x_test[numeric_features] = scaler.transform(self.x_test[numeric_features])

        return self.x_train, self.x_test, self.y_train, self.y_test

    def data_filter(self) -> list:
        if not self.splited:
            print('Data not splited, please split the data first')
            return []

        # 必须包含的关键特征
        required_features = [
            'annual_inc', 'collections_12_mths_ex_med', 'delinq_2yrs', 'dti',
            'funded_amnt', 'pub_rec', 'sub_grade', 'term',
            'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal'
        ]

        # 根据模式筛选特征
        if self.mode == "random":
            # 随机选择前 15 个特征
            selected_features = self.x_train.columns.to_list()[:15]

        elif self.mode == "catboost":
            from catboost import CatBoostClassifier, Pool
            # 获取类别特征的列名
            categorical_features = self.x_train.select_dtypes(include=['object']).columns.tolist()

            # 定义数据池
            train_pool = Pool(data=self.x_train, label=self.y_train, cat_features=categorical_features)

            # 初始化并训练模型
            model = CatBoostClassifier(iterations=100, learning_rate=0.1, depth=6, verbose=False)
            model.fit(train_pool)

            # 获取特征重要性
            importances = model.get_feature_importance()
            feature_names = self.x_train.columns
            feature_importance = pd.DataFrame({'feature': feature_names, 'importance': importances})

            # 按重要性排序，选择前 15 个特征
            feature_importance.sort_values(by='importance', ascending=False, inplace=True)
            selected_features = feature_importance.head(15)['feature'].tolist()

            print(f"Selected features ({len(selected_features)}): {selected_features}")

        # 添加关键特征
        selected_features = self.add_required_features(selected_features, required_features)

        # 更新过滤后的数据
        self.x_train_filtered = self.x_train[selected_features]
        self.x_test_filtered = self.x_test[selected_features]

        # 返回筛选后的数据和标签
        self.filtered = True
        return [self.x_train_filtered, self.x_test_filtered, self.y_train, self.y_test]

    def add_required_features(self, selected_features: list, required_features: list) -> list:
        for feature in required_features:
            if feature not in selected_features:
                selected_features.append(feature)
        return selected_features

    def get_data(self) -> pd.DataFrame:
        return self.data

    def get_splited_data(self) -> tuple:
        if not self.splited:
            print('Data not splited, please split the data first')
            return None, None, None, None
        return self.x_train, self.x_test, self.y_train, self.y_test

    def get_filtered_data(self) -> tuple:
        if not self.filtered:
            print('Data not filtered, please filter the data first')
            return None, None, None, None
        return self.x_train_filtered, self.x_test_filtered, self.y_train, self.y_test