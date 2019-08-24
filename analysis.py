from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.manifold
import os

par_dir = os.path.join(os.path.dirname(__file__))
raw_data_dir = os.path.join(par_dir,r"data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv")
country_dir = os.path.join(par_dir, r'data/raw/country-group.xls')
data_save_dir = os.path.join(par_dir, r'data/processed/dataset.csv')
name = "dataset_decomposition"
plot_dir = os.path.join(par_dir, r'reports/figures/scatter_')

data_cut = .1
param_vals = (name, data_cut)
processed_save_path = os.path.join(par_dir, "data/processed/%sCut%s.csv" % param_vals)

if not os.path.exists(processed_save_path):
    food_data = UN_food(
        raw_dir=raw_data_dir,
        country_dir=country_dir)
    food_data.clean_data(data_ratio_cut=data_cut)
    food_data.write_data(save_dir=processed_save_path)

dim_reduction = Reduction(processed_data_dir=processed_save_path,)

tsne_save_path = os.path.join(par_dir, "data/processed/tsne%sCut%s.csv" % param_vals)
dim_reduction.fit_transform(
    reduced_data_dir=tsne_save_path,
    method = sklearn.manifold.TSNE(verbose = 2,random_state = 11)
)

scatter_plots = Scatter(
    bidimensional_dataset = tsne_save_path
)


plot_dir = os.path.join(par_dir, r'reports/figures/scatter_Cut%s%s' % param_vals)

scatter_plots.plot(
    file_dir_prefix = plot_dir,
    years=list(range(1961,2014)),
    extension = '.png'
)