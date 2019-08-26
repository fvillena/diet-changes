import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.preprocessing
import sklearn.decomposition
import os


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





    def clean_euro_data(self, euro_dir, standard = sklearn.preprocessing.StandardScaler(),
                        data_ratio_cut_columns=.05, data_ratio_cut_rows=.05,
                        countries_to_drop=["Bolivia", "El Salvador","Honduras", "Panama", "Paraguay"]):

        for country in countries_to_drop:
            self.processed_data = self.processed_data.drop(self.processed_data[self.processed_data["Area"]==country].index)
        self.processed_data = self.processed_data[self.processed_data["Year"] != 2004]
        self.food_info = self.processed_data
        self.zero_as_na = False





        self.data_ratio_cut_columns = data_ratio_cut_columns
        self.data_ratio_cut_rows = data_ratio_cut_rows


        self.processed_data["Continent"] = self.processed_data["Area"].map(self.continents)
        # if self.zero_as_na:
        #     self.food_info.replace(0,np.nan, inplace=True)
        self.food_pivot = self.food_info.dropna(thresh=int(self.food_info.shape[0]*(1-self.data_ratio_cut_columns)), axis=1)
        # self.food_pivot = self.food_info.dropna(thresh=int(self.food_info.shape[1]*(1-self.data_ratio_cut_rows)), axis=0)
        # self.food_pivot.sort_values(by=sort_keys, inplace=True)


        # self.food_pivot.fillna(method='backfill', inplace=True)
        # self.food_pivot.fillna(method='ffill', inplace=True)


        for col in self.food_pivot.columns[3:]:
            if col == "Sports Drinks":
                asfd=34
            if (self.food_pivot[col].dtype == "object"):
                self.food_pivot[col] = self.food_pivot[col].str.replace(",",'')
            self.food_pivot[col].fillna(self.food_pivot[col].median(), inplace=True)
        asas=363636

        self.food_pivot[self.food_pivot.columns[3:]] = standard.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])
        self.food_pivot = self.food_pivot.reset_index(drop=True)
        awer=2134



    def PCA_analysis(self, method=sklearn.decomposition.PCA(2), reduced_data_dir=r'../data/processed/dataset_2d_pca.csv'):

        data_2d = method.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])
        data_2d = pd.concat([self.food_pivot[['Area','Year']], pd.DataFrame(data_2d)], axis=1)
        data_2d.columns = ['Area','Year', 'x', 'y']

        self.PCAComp = pd.DataFrame(method.components_, columns=self.food_pivot.columns[3:], index=['PC-1', 'PC-2'])
        # data_2d.to_csv(reduced_data_dir,index=False)
        self.data_2d = data_2d


    def clean_data(self, data_ratio_cut_columns=0.05,data_ratio_cut_rows=0.05, sort_keys=['Area', 'Continent','Year Code'], zero_as_na=False,
                   standard = sklearn.preprocessing.StandardScaler()):

        self.food_info = self.processed_data[self.processed_data["Element Code"].isin([645])]

        if True:
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


        self.food_pivot_not_scaled = self.food_pivot.copy()
        self.food_pivot[self.food_pivot.columns[3:]] = self.standardizer.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])







    def write_data(self, save_dir=r'~/PycharmProjects/diet-changes/data/processed/dataset3.csv', save_dir_unscaled=r'~/PycharmProjects/diet-changes/data/processed/dataset3.csv'):
        self.food_pivot.to_csv(save_dir, index=False)
        self.food_pivot_not_scaled.to_csv(save_dir_unscaled, index=False)


    def plot_PCA_overtime(self, plot_dir):

        years = self.data_2d["Year"].unique()
        countries = self.data_2d["Area"].unique()

        save_dir = os.path.join(plot_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for year in years:
            # fig, ax = plt.subplots(figsize=(30, 30))

            for country in countries:
                coun_dat = self.data_2d[self.data_2d["Area"]==country][self.data_2d["Year"]==year]

                plt.scatter(coun_dat["x"], coun_dat["y"])
                plt.text(coun_dat["x"], coun_dat["y"], country)

            plt.title('Projection of Food Consumptions in ' + str(year))
            plt.xlim(self.data_2d['x'].min(), self.data_2d['x'].max())
            plt.ylim(self.data_2d['y'].min(), self.data_2d['y'].max())
            # plt.legend()
            plt.tight_layout()

            full_file_path = os.path.join(save_dir, str(year) + ".png")

            plt.savefig(full_file_path)

            plt.clf()
        asdb=234
