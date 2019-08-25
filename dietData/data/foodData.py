import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.preprocessing

class UN_food():
    def __init__(self, raw_dir=r'~/PycharmProjects/diet-changes/data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv',
                 country_dir=r'~/PycharmProjects/diet-changes/data/raw/country-group.xls', rem_noISO2=True, constrain_food_info=True,
                 standard = sklearn.preprocessing.StandardScaler()):

        self.raw_data = pd.read_csv(raw_dir, encoding='latin-1')
        self.processed_data = pd.read_csv(raw_dir, encoding='latin-1')

        country = pd.read_excel(country_dir)

        cont = list(zip(country['Country'],country['Country Group']))
        self.continents = {key:val for key,val in cont}

        self.countries = country[country['ISO2 Code'].isna() == False]['Country Code'].tolist()

        self.processed_data["Continent"] = self.raw_data["Area"].map(self.continents)

        self.food_info = self.processed_data[self.processed_data["Element Code"].isin([5301,511])]

        if constrain_food_info:
            self.food_info = self.food_info[[
                'Area',
                'Continent',
                'Item',
                'Year Code',
                'Value'
            ]]

        self.food_pivot = pd.pivot_table(self.food_info,
                                         values='Value',
                                         index=['Area','Continent','Year Code'],
                                         columns=['Item']).reset_index()

        self.standardizer = standard





    def clean_data(self, data_ratio_cut_columns=0.05,data_ratio_cut_rows=0.05, sort_keys=['Area', 'Continent','Year Code'], zero_as_na=False):

        self.zero_as_na = zero_as_na

        self.data_ratio_cut_columns = data_ratio_cut_columns
        self.data_ratio_cut_rows = data_ratio_cut_rows


        self.processed_data["Continent"] = self.processed_data["Area"].map(self.continents)
        if self.zero_as_na:
            self.food_pivot.replace(0,np.nan, inplace=True)
        self.food_pivot = self.food_pivot.dropna(thresh=int(self.food_pivot.shape[0]*(1-self.data_ratio_cut_columns)), axis=1)
        self.food_pivot = self.food_pivot.dropna(thresh=int(self.food_pivot.shape[1]*(1-self.data_ratio_cut_rows)), axis=0)
        self.food_pivot.sort_values(by=sort_keys, inplace=True)
        self.food_pivot.fillna(method='backfill', inplace=True)
        self.food_pivot.fillna(method='ffill', inplace=True)


        self.food_pivot[self.food_pivot.columns[3:]] = \
            self.food_pivot[self.food_pivot.columns[3:]].divide(self.food_pivot.Population, axis=0)

        self.food_pivot.drop(columns ='Population', inplace=True)

        self.food_pivot_not_scaled = self.food_pivot.copy()
        self.food_pivot[self.food_pivot.columns[3:]] = self.standardizer.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])






    def write_data(self, save_dir=r'~/PycharmProjects/diet-changes/data/processed/dataset3.csv', save_dir_unscaled=r'~/PycharmProjects/diet-changes/data/processed/dataset3.csv'):
        self.food_pivot.to_csv(save_dir, index=False)
        self.food_pivot_not_scaled.to_csv(save_dir_unscaled, index=False)

