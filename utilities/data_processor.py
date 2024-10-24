import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
try: import gdown 
except ImportError: exit('Please install gdown by running: pip install gdown')


class DataProcessor():
    def __init__(self, input_name: str = 'data.csv', output_name: str = 'cleaned_data.csv', data_folder: str = './dataset'):
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

    def show_data_info(self, n: int = 5):
        if not self.loaded:
            print('Data not loaded, please load the data first')
            return
        # print the shape of the data
        print(f'processed: {self.processed}')
        print(f'data shape: {self.data.shape}')
        self.data.info()
        print(f'data head: \n {self.data.head(n)}')
        return

    def load_data(self, download: bool = False):
        if not os.path.exists(self.input_path) and not download:
            print('File does not exist, be sure to turn on download or check the input path, current path is: ', self.input_path)
            return
        elif not os.path.exists(self.input_path) and download:
            url: str = 'https://drive.google.com/uc?id=1DgyuTGhIlQ4nwHBkXhwk5FAoCSgR_acZ'
            gdown.download(url, self.input_path, quiet=False)
        
        self.data: pd.DataFrame = pd.read_csv(self.input_path, index_col=0)
        self.processed: bool = False
        return 
