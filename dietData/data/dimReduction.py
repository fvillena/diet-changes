import numpy as np
import pandas as pd
import sklearn.decomposition
import sklearn.manifold

class Reduction():
    def __init__(
        self,
        processed_data_dir=r'../data/processed/dataset.csv',
        methods=[
            ('pca', sklearn.decomposition.PCA(2)),
            ('tsne', sklearn.manifold.TSNE(verbose = 2, random_state = 11))
        ]
    ):

        self.processed_data = pd.read_csv(processed_data_dir)
        self.methods = methods

    def fit_transform(
        self,
        reduced_data_dir=r'../data/processed/'
    ):
        for name,method in self.methods:
            data_2d = method.fit_transform(self.processed_data[self.processed_data.columns[2:]])
            data_2d = pd.concat([self.processed_data[['Area','Continent','Year Code']], pd.DataFrame(data_2d)], axis=1)
            data_2d.columns = ['Area','Continent','Year Code', 'PC1', 'PC2']
            data_2d.to_csv(
                reduced_data_dir + 'dataset_2d_' + name + '.csv',
                index=False
            )