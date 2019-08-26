from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.decomposition
import sklearn.preprocessing
import os
import matplotlib.pyplot as plt
import pandas as pd


#get the parent directory of where the file is being executed
par_dir = os.path.join(os.path.dirname(__file__))
country_dir = os.path.join(par_dir, "data", "raw", "country-group.xls")
standard = sklearn.preprocessing.StandardScaler()
stan_str = "Standard"
data_cut = .05




america_dir = os.path.join(par_dir, "data", "raw", "americaPreprocessed2.csv")

america_food_data = UN_food(raw_dir=america_dir,
                            country_dir=country_dir)




america_food_data.clean_euro_data(america_dir,
                                  data_ratio_cut_columns=data_cut,
                                  standard=standard)

america_food_data.PCA_analysis()
america_plot_dir = os.path.join(par_dir, "reports","figures", "rowCut%sAmericas_standard%s_NANMedian"
                                % (america_food_data.data_ratio_cut_rows, stan_str))
america_food_data.plot_PCA_overtime(plot_dir=america_plot_dir)


asdf=343

# euro_dir = os.path.join(par_dir, "data", "raw", "europePreprocessed2.csv")
#
# europe_food_data = UN_food(raw_dir=euro_dir,
#                             country_dir=country_dir)
#
#
# europe_food_data.clean_euro_data(euro_dir,
#                                   data_ratio_cut_columns=data_cut,
#                                  standard=standard)
#
# europe_food_data.PCA_analysis()
# europe_plot_dir = os.path.join(par_dir, "reports","figures", "rowCut%sEurope_standard%s_NANMedian"
#                                % (europe_food_data.data_ratio_cut_rows,stan_str))
# europe_food_data.plot_PCA_overtime(plot_dir=europe_plot_dir)
#
#
# eurAmer_dir = os.path.join(par_dir, "data", "raw", "europePreprocessed2.csv")
#
# eurAmer_food_data = UN_food(raw_dir=eurAmer_dir,
#                             country_dir=country_dir)
#
#
# eurAmer_food_data.clean_euro_data(eurAmer_dir,
#                                   data_ratio_cut_columns=data_cut,
#                                   standard=standard)
#
# eurAmer_food_data.PCA_analysis()
# eurAmer_plot_dir = os.path.join(par_dir, "reports","figures", "rowCut%sEuropeAndAmerica_standard%s_NANMedian"
#                                 % (eurAmer_food_data.data_ratio_cut_rows,stan_str))
# eurAmer_food_data.plot_PCA_overtime(plot_dir=eurAmer_plot_dir)

asdf=234




asdf=348747

