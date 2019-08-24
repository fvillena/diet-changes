import numpy as np
import pandas as pd
import sklearn.preprocessing
import matplotlib.pyplot as plt
import os
class Scatter:
    def __init__(
        self,
        bidimensional_dataset,
    ):
        self.dataset = pd.read_csv(bidimensional_dataset)
        self.le = sklearn.preprocessing.LabelEncoder()
        self.dataset['Continent'] = self.le.fit_transform(self.dataset['Continent'])

    def plot(self,years = [1980,2010],file_dir_prefix = r'../../report/figures/scatter_',epsilon = 0.005,extension = '.png'):

        save_dir = os.path.join(file_dir_prefix)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for year in years:
            fig, ax = plt.subplots(figsize=(30,30))

            for continent in self.le.classes_:
                ax.scatter(self.dataset[self.dataset['Year Code'] == year][self.dataset['Continent'] == self.le.transform([continent])[0]]['x'],
                        self.dataset[self.dataset['Year Code'] == year][self.dataset['Continent'] == self.le.transform([continent])[0]]['y'],
                        label = continent
                        )
            for key, row in self.dataset[self.dataset['Year Code'] == year].iterrows():
                ax.annotate(row['Area'], xy=(row['x']+epsilon, row['y']))

            ax.set_title('Projection of Food Consumptions in ' + str(year))
            ax.set_xlim(self.dataset['x'].min(), self.dataset['x'].max())
            ax.set_ylim(self.dataset['y'].min(), self.dataset['y'].max())
            ax.legend()
            fig.tight_layout()

            full_file_path = os.path.join(save_dir, str(year) + extension)


            fig.savefig(full_file_path)