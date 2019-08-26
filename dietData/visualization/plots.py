import numpy as np
import pandas as pd
import sklearn.preprocessing
import matplotlib.pyplot as plt
import os
import scipy.spatial
class Scatter:
    def __init__(
        self,
        bidimensional_dataset,
    ):
        self.dataset = pd.read_csv(bidimensional_dataset)
        self.le = sklearn.preprocessing.LabelEncoder()
        self.dataset['Continent'] = self.le.fit_transform(self.dataset['Continent'])

    def plot(self,years = [1980,2010],file_dir_prefix = r'../../report/figures/scatter_',border = 1,epsilon = 0.2,extension = '.png'):

        save_dir = os.path.join(file_dir_prefix)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        continent_data = self.dataset.groupby(by=['Continent','Year Code']).agg('median').reset_index()
        for year in years:
            points = continent_data[continent_data['Year Code'] == year][['x','y']]
            vor = scipy.spatial.Voronoi(points)
            fig, ax = plt.subplots(figsize=(30,30))

            for continent in self.le.classes_:
                ax.scatter(self.dataset[self.dataset['Year Code'] == year][self.dataset['Continent'] == self.le.transform([continent])[0]]['x'],
                        self.dataset[self.dataset['Year Code'] == year][self.dataset['Continent'] == self.le.transform([continent])[0]]['y'],
                        label = continent,
                        s=300
                        )
            for _, row in self.dataset[self.dataset['Year Code'] == year].iterrows():
                ax.annotate(row['Area'], xy=(row['x']+epsilon, row['y']))
            scipy.spatial.voronoi_plot_2d(
                vor,ax,
                show_points=False,
                show_vertices = False
            )
            ax.set_title('Projection of Food Consumptions in ' + str(year))
            ax.set_xlim(self.dataset['x'].min()-border, self.dataset['x'].max()+border)
            ax.set_ylim(self.dataset['y'].min()-border, self.dataset['y'].max()+border)
            ax.legend()
            fig.tight_layout()

            full_file_path = os.path.join(save_dir, str(year) + extension)


            fig.savefig(full_file_path)

            fig.clf()
class Line:
    def __init__(
        self,
        not_normalized_dataset
    ):
        self.dataset = pd.read_csv(not_normalized_dataset)
        self.foods = self.dataset.columns[3:]

    def plot(self, countries,file_dir_prefix = r'../../report/figures/line_',extension = '.png'):
        save_dir = os.path.join(file_dir_prefix)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.grouped_dataset = self.dataset.groupby(by='Year Code').agg('mean')
        for food in self.foods:
            plt.plot(
                self.grouped_dataset.reset_index()['Year Code'],
                self.grouped_dataset[food], 
                label='Mean', 
                linestyle='--',  
                alpha=0.5
            )
            for country in countries:
                plt.plot(
                self.dataset[self.dataset.Area == country]['Year Code'],
                self.dataset[self.dataset.Area == country][food],
                label = country
            )
            plt.title(food)
            plt.xlabel('Year')
            plt.ylabel('Per capita consumption (kg)')
            plt.tight_layout()
            plt.legend()

            full_file_path = os.path.join(save_dir, str(food) + extension)


            plt.savefig(full_file_path)

            plt.clf()

