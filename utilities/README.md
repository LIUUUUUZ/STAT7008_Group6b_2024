# Utilities 中可调用模块的使用说明       
### Utilities的调用方式为在项目文件夹中调用import utilities 再调用其中的方法, 子文件夹中调用会失效（因为不在package文件夹中，后续可以设置）
1. DataPreProcessor， 用于加载数据，清洗数据，储存后续训练要用的数据。    
    1. 初始化需要输入input_name：原始数据名称(xxxx/xxxx.csv)， output_name：若需要，保存数据的名称， data_folder: 储存文件的文件夹。
    2. show_data_info(), 输出data的详细数据。
    3. load_data(self, download: bool = False)， 用于加载数据，若希望直接下载则请设置为True。
    4. preprocess_data() 细节请自行阅读代码， 用于加工数据， 填补缺失值时有众数，平均数，0 和删去整列四种方式
    5. show_feature_plt() 展示数据的各特质分布

2. DataLoader， 用于数据深度加工生成训练数据集
    1. 初始化需要输入由DataPreProccessor生成的DataFrame
    2. encoder() 将数据中object encode成数字
    3. split_data() 数据划分， 可设置不同的数据集大小
    4. data_filter(mode) 数据深度筛选， 目前支持random: 选取最前15个特征；
    5. 一些功能函数， 详细见代码