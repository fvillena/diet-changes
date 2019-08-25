from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.manifold
import os
import matplotlib.pyplot as plt

par_dir = os.path.join(os.path.dirname(__file__))

data_save_dir = os.path.join(par_dir,"data","processed","dataset.csv")
name = "dataset_decomposition"
plot_dir = os.path.join(par_dir, "reports","figures","scatter_")

data_cut = .01
random_seed = 120
param_vals = (name, data_cut)
processed_save_path = os.path.join(par_dir, "data","processed","%sCut%s.csv" % param_vals)

if not os.path.exists(processed_save_path):
    raw_data_dir = os.path.join(par_dir, "data", "raw", "FoodBalanceSheets_E_All_Data_(Normalized).csv")
    country_dir = os.path.join(par_dir, "data", "raw", "country-group.xls")
    food_data = UN_food(
        raw_dir=raw_data_dir,
        country_dir=country_dir)
    food_data.clean_data(data_ratio_cut=data_cut)
    food_data.write_data(save_dir=processed_save_path)
else:
    food_data = Reduction(processed_data_dir=processed_save_path, )

food_data.correlation_finder()

tsne_save_path = os.path.join(par_dir, "data","processed","tsne%sCut%srandSeed%s.csv" % (name, data_cut, random_seed))



food_data.fit_transform(reduced_data_dir=tsne_save_path,method = sklearn.manifold.TSNE(verbose = 2,random_state = random_seed))

# plt.plot(food_data.food_pivot[food_data.food_pivot["Area"]=="United States of America"]["Cereals, Other"])


scatter_plots = Scatter(
    bidimensional_dataset = tsne_save_path
)
# for country in self.dataset["Area"].unique():
#     plt.plot(self.dataset[self.dataset["Area"]==country].diff(axis=1)['x'], self.dataset[self.dataset["Area"]==country].diff(axis=1)['y'], 'o')

plot_dir = os.path.join(par_dir, "reports","figures", "scatter_Cut%s%s" % param_vals)

scatter_plots.plot(
    file_dir_prefix = plot_dir,
    years=list(range(1961,2014)),
    extension = '.png'
)