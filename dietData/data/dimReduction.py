import numpy as np
import pandas as pd
import sklearn.decomposition
import json

class Reduction():
    def __init__(self,processed_data_dir=r'../data/processed/dataset.csv',):

        self.processed_data = pd.read_csv(processed_data_dir)
        asdf=2309239

    def fit_transform(self,method=sklearn.decomposition.PCA(2),reduced_data_dir=r'../data/processed/dataset_2d_pca.csv'):
        self.method = method
        data_2d = method.fit_transform(self.processed_data[self.processed_data.columns[3:]])
        data_2d = pd.concat([self.processed_data[['Area','Continent','Year Code']], pd.DataFrame(data_2d)], axis=1)
        data_2d.columns = ['Area','Continent','Year Code', 'x', 'y']
        data_2d.to_csv(reduced_data_dir,index=False)

    def make_report(self, report_path):
        if type(self.method).__name__ == 'PCA':
            pc1_weights = sorted(list(zip(self.processed_data[self.processed_data.columns[3:]],self.method.components_[0])), key=lambda x: abs(x[1]), reverse=True)
            pc2_weights = sorted(list(zip(self.processed_data[self.processed_data.columns[3:]],self.method.components_[1])), key=lambda x: abs(x[1]), reverse=True)
            report = {
                'pc1_weights' : pc1_weights,
                'pc2_weights' : pc2_weights
            }
        else:
            report: {

            }
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
    def correlation_finder(self):
        asdf=34