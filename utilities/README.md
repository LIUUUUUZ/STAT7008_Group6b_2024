# Utilities 中可调用模块的使用说明       
### Utilities的调用方式为在项目文件夹中调用import utilities 再调用其中的方法, 子文件夹中调用会失效（因为不在package文件夹中，后续可以设置）
1. DataProcessor， 用于加载数据，清洗数据，储存后续训练要用的数据。    
    1. 初始化需要输入input_name：原始数据名称(xxxx/xxxx.csv)， output_name：若需要，保存数据的名称， data_folder: 储存文件的文件夹。
    2. show_data_info(), 输出data的详细数据。
    3. load_data(self, download: bool = False)， 用于加载数据，若希望直接下载则请设置为True。
