import numpy as np
from sklearn.decomposition import PCA
from dietData.data.foodData import UN_food

food_data = UN_food()
food_data.clean_data()
food_data.write_data()

sdf=234