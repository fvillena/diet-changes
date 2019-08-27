import numpy as np
import pandas as pd
import json
def euclideanDistance(a,b):
    return np.linalg.norm(a-b)
def distance(v1,v2,metric):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return metric(v1,v2)
class Movement:
    def __init__(self, bidimensional_dataset):
        self.bidimensional_dataset = pd.read_csv(bidimensional_dataset)
        self.countries = list(set(self.bidimensional_dataset.Area.values))
    def calculate_save(self,destination_path):
        movements = []
        for country in self.countries:
            distances = []
            positions = []
            for _,row in self.bidimensional_dataset[self.bidimensional_dataset.Area == country].iterrows():
                positions.append((row['x'],row['y']))
            for i in range(1,len(positions)):
                d = distance(positions[i-1], positions[i], euclideanDistance)
                distances.append(d)
            movement = sum(distances)
            movements.append((country,movement))
        movements = sorted(movements, key=lambda x: x[1], reverse=True)
        pd.DataFrame(movements,columns=['country','displacement']).to_csv(destination_path, index=False)