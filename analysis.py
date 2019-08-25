from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.decomposition
import sklearn.preprocessing
import os
import matplotlib.pyplot as plt

par_dir = os.path.join(os.path.dirname(__file__))
raw_data_dir = os.path.join(par_dir,r"data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv")
country_dir = os.path.join(par_dir, r'data/raw/country-group.xls')
plot_dir = os.path.join(par_dir, r'reports/figures/scatter_')

dim_reduction_method = ("pca" ,sklearn.decomposition.PCA(2))
data_cut_columns = .05
data_cut_rows = .05
zero_as_na = True
scaler = ("minmax",sklearn.preprocessing.MinMaxScaler())

data_save_dir = os.path.join(par_dir,"data","processed","dataset.csv")
name = "dataset_decomposition"
plot_dir = os.path.join(par_dir, "reports","figures","scatter_")

param_vals = (dim_reduction_method[0], scaler[0], str(data_cut_columns), str(data_cut_rows), str(zero_as_na))
processed_scaled_save_path = os.path.join(par_dir, r"data/processed/dataset_scaler-%s_cut-%s-%s_zanan-%s.csv" % param_vals[1:])
processed_unscaled_save_path = os.path.join(par_dir, r"data/processed/dataset_cut-%s-%s_zanan-%s.csv" % param_vals[2:])
dataset_2d_save_path = os.path.join(par_dir, r"data/processed/dataset_2d_reduction-%s_scaler-%s_cut-%s-%s_zanan-%s.csv" % param_vals)
plot_dir = os.path.join(par_dir, r'reports/figures/scatter_reduction-%s_scaler-%s_cut-%s-%s_zanan-%s' % param_vals)


food_data = UN_food(
    raw_dir=raw_data_dir,
    country_dir=country_dir,
    standard=scaler[1])
food_data.clean_data(data_ratio_cut_columns=data_cut_columns, data_ratio_cut_rows=data_cut_rows, zero_as_na=True)
food_data.write_data(save_dir=processed_scaled_save_path, save_dir_unscaled=processed_unscaled_save_path)

dim_reduction = Reduction(processed_data_dir=processed_scaled_save_path)

dim_reduction.fit_transform(
    reduced_data_dir=dataset_2d_save_path,
    method = dim_reduction_method[1]
)

scatter_plots = Scatter(
    bidimensional_dataset = dataset_2d_save_path
)

plot_dir = os.path.join(par_dir, "reports","figures", "scatter_Cut%s%s" % param_vals)

scatter_plots.plot(
    file_dir_prefix = plot_dir,
    years=list(range(1961,2014)),
    extension = '.png'
)

adsf=234