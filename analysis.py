from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.decomposition
import os

par_dir = os.path.join(os.path.dirname(__file__))
raw_data_dir = os.path.join(par_dir,r"data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv")
country_dir = os.path.join(par_dir, r'data/raw/country-group.xls')
data_save_dir = os.path.join(par_dir, r'data/processed/dataset.csv')
dim_reduction_method = ("pca" ,sklearn.decomposition.PCA(2))
plot_dir = os.path.join(par_dir, r'reports/figures/scatter_')

data_cut_columns = .05
data_cut_rows = .05
zero_as_na = True
param_vals = (dim_reduction_method[0], str(data_cut_columns), str(data_cut_rows), str(zero_as_na))
processed_save_path = os.path.join(par_dir, "data/processed/dataset_cut-%s-%s_zanan-%s.csv" % param_vals[1:])

# food_data = UN_food(
#     raw_dir=raw_data_dir,
#     country_dir=country_dir)
# food_data.clean_data(data_ratio_cut_columns=data_cut_columns, data_ratio_cut_rows=data_cut_rows, zero_as_na=True)
# food_data.write_data(save_dir=processed_save_path)

dim_reduction = Reduction(processed_data_dir=processed_save_path)

dataset_2d_save_path = os.path.join(par_dir, "data/processed/dataset_2d_%s_cut-%s-%s_zanan-%s.csv" % param_vals)
dim_reduction.fit_transform(
    reduced_data_dir=dataset_2d_save_path,
    method = dim_reduction_method[1]
)

scatter_plots = Scatter(
    bidimensional_dataset = dataset_2d_save_path
)


plot_dir = os.path.join(par_dir, r'reports/figures/scatter_%s_cut-%s-%s_zanan-%s' % param_vals)

scatter_plots.plot(
    file_dir_prefix = plot_dir,
    years=list(range(1961,2014)),
    extension = '.png'
)