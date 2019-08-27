import numpy as np
import pandas as pd
import scipy.spatial.distance

class Fitting:
    def __init__(self, bidimensional_dataset_path):
        self.data = pd.read_csv(bidimensional_dataset_path)
        self.continents = {}
        for _,row in self.data.iterrows():
            self.continents[row['Area']] = row['Continent']
        self.years = list(set(self.data['Year Code'].values))
    def analyze_fitting(self, result_path):
        metrics_total = []
        for year in self.years:
            positions = np.array(self.data[self.data['Year Code'] == year][['x','y']])
            countries = self.data[self.data['Year Code'] == year].Area.values
            distances = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(positions))
            lookupTable, _ = np.unique(countries, return_inverse=True)
            neighbors = pd.DataFrame(list(zip(
                countries,
                lookupTable[np.argsort(distances,axis=0)[1]],
                lookupTable[np.argsort(distances,axis=0)[2]],
                lookupTable[np.argsort(distances,axis=0)[3]],
                lookupTable[np.argsort(distances,axis=0)[4]],
                lookupTable[np.argsort(distances,axis=0)[5]],
            )),columns=['country']+list(range(0,5)))
            for i in range(5):
                neighbors[i] = neighbors[i].map(self.continents)
            neighbors['continent'] = neighbors.country.map(self.continents)
            for _,row in neighbors.iterrows():
                current_neighbors = [row[i] for i in range(5)]
                metric = current_neighbors.count(row['continent'])/5
                metrics_total.append((row['country'],year,metric))
        metrics_total = pd.DataFrame(metrics_total,columns=['country','year','metric'])
        # metrics_total = pd.pivot_table(metrics_total,
        #     values='metric',
        #     index='country',
        #     columns='year').reset_index()
        metrics_total.to_csv(result_path, index=False)
