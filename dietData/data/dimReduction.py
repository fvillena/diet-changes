import numpy as np
import pandas as pd
import sklearn.decomposition

class Reduction():
    def __init__(
        self,
        processed_data_dir=r'../data/processed/dataset.csv',
    ):

        self.processed_data = pd.read_csv(processed_data_dir)

    def fit_transform(self,method=sklearn.decomposition.PCA(2),reduced_data_dir=r'../data/processed/dataset_2d_pca.csv'):

        data_2d = method.fit_transform(self.processed_data[self.processed_data.columns[3:]])
        data_2d = pd.concat([self.processed_data[['Area','Continent','Year Code']], pd.DataFrame(data_2d)], axis=1)
        data_2d.columns = ['Area','Continent','Year Code', 'x', 'y']
        data_2d.to_csv(
            reduced_data_dir,
            index=False
)