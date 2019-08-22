import numpy as np
from sklearn.decomposition import PCA
from dietData.data.foodData import UN_food

food_data = UN_food()
food_data.clean_data()
food_data.write_data()

sdf=234


piciei = PCA(2)

data_2d_pca = piciei.fit_transform(data[data.columns[2:]])
data_2d_pca = pd.concat([data[['Area','Continent','Year Code']], pd.DataFrame(data_2d_pca)], axis=1)
data_2d_pca.columns = ['Area','Continent','Year Code', 'PC1', 'PC2']