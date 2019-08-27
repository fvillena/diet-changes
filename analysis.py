from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
from dietData.visualization.plots import Line
from dietData.analysis.movement import Movement
import sklearn.decomposition
import sklearn.preprocessing
import os
import matplotlib.pyplot as plt

par_dir = os.path.join(os.path.dirname(__file__))
raw_data_dir = os.path.join(par_dir,r"data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv")
country_dir = os.path.join(par_dir, r'data/raw/country-group.xls')
scatter_plot_dir = os.path.join(par_dir, r'reports/figures/scatter_')


dim_reduction_method = ("pca" ,sklearn.decomposition.PCA(2))
data_cut_columns = .05
data_cut_rows = .05
zero_as_na = False
scaler = ("minmax",sklearn.preprocessing.MinMaxScaler())
continent = None

param_vals = (dim_reduction_method[0], scaler[0],str(continent), str(data_cut_columns), str(data_cut_rows), str(zero_as_na))

processed_dir = os.path.join("data","processed")

if not os.path.exists(os.path.join(par_dir,processed_dir)):
    os.makedirs(os.path.join(par_dir,processed_dir))

processed_scaled_save_path = os.path.join(par_dir, processed_dir,"dataset_scaler-%s_continent-%s_cut-%s-%s_zanan-%s.csv" % param_vals[1:])
processed_unscaled_save_path = os.path.join(par_dir, processed_dir, "dataset_continent-%s_cut-%s-%s_zanan-%s.csv" % param_vals[2:])
dataset_2d_save_path = os.path.join(par_dir, processed_dir, "dataset_2d_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s.csv" % param_vals)
scatter_plot_dir = os.path.join(par_dir, "reports","figures","scatter_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s" % param_vals)
line_plot_dir = os.path.join(par_dir, "reports","figures","line_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s" % param_vals)
preprocessing_report_path = os.path.join(par_dir, "reports", "preprocessing-report_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s.json" % param_vals)
reduction_report_path = os.path.join(par_dir, "reports", "reduction-report_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s.json" % param_vals)
movement_report_path = os.path.join(par_dir, "reports", "movement-report_reduction-%s_scaler-%s_continent-%s_cut-%s-%s_zanan-%s.json" % param_vals)



# raw_data_dir = os.path.join(par_dir, "data", "raw", "FoodBalanceSheets_E_All_Data_(Normalized).csv")
# country_dir = os.path.join(par_dir, "data", "raw", "country-group.xls")
# food_data = UN_food(
#     raw_dir=raw_data_dir,
#     country_dir=country_dir,
#     continent = continent)
# food_data.clean_data(data_ratio_cut_columns=data_cut_columns)
# food_data.make_report(report_path=preprocessing_report_path)
# food_data.write_data(save_dir=processed_scaled_save_path, save_dir_unscaled=processed_unscaled_save_path)



# dim_reduction = Reduction(processed_data_dir=processed_scaled_save_path)

# dim_reduction.fit_transform(
#     reduced_data_dir=dataset_2d_save_path,
#     method = dim_reduction_method[1]
# )

# dim_reduction.make_report(report_path=reduction_report_path)

movement_analyzer = Movement(dataset_2d_save_path)
movement_analyzer.calculate_save(movement_report_path)

# line_plots = Line(
#     not_normalized_dataset = processed_unscaled_save_path
# )


# line_plots.plot(
#     file_dir_prefix = line_plot_dir,
#     countries=['Chile','United States of America'],
#     extension = '.png'
# )

# scatter_plots = Scatter(
#     bidimensional_dataset = dataset_2d_save_path
# )


# scatter_plots.plot(
#     voronoi = True,
#     file_dir_prefix = scatter_plot_dir,
#     years=list(range(1961,2014)),
#     extension = '.png'
# )

