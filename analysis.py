from dietData.data.foodData import UN_food
from dietData.data.dimReduction import Reduction

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
    reduced_data_dir=r'data/processed/'
)