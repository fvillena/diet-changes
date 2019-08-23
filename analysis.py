from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction
from dietData.visualization.plots import Scatter
import sklearn.manifold

food_data = UN_food(
    raw_dir=r'data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv',
    country_dir=r'data/raw/country-group.xls'
)
food_data.clean_data()
food_data.write_data(
    save_dir=r'data/processed/dataset.csv'
)

dim_reduction = Reduction(
    processed_data_dir=r'data/processed/dataset.csv',
)

dim_reduction.fit_transform(
    reduced_data_dir=r'data/processed/dataset_2d_tsne.csv',
    method = sklearn.manifold.TSNE(
        verbose = 2,
        random_state = 11
    )
)

scatter_plots = Scatter(
    bidimensional_dataset = r'data/processed/dataset_2d_tsne.csv'
) 
scatter_plots.plot(
    file_dir_prefix = r'reports/figures/scatter_',
    years=list(range(1961,2014)),
    extension = '.png'
)