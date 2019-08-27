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
                        countries_to_drop=["Bolivia", "El Salvador","Honduras", "Panama", "Paraguay"],
                        foods_to_drop=["Sports Drinks","RTD Coffee", "Concentrates"]):

        for country in countries_to_drop:
            self.processed_data = self.processed_data.drop(self.processed_data[self.processed_data["Area"]==country].index)

        for food in foods_to_drop:
            self.processed_data = self.processed_data[self.processed_data.columns[self.processed_data.columns != food]]

        # [np.where(self.food_pivot.isnull().values)]

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

        # Correlation analysys
        fc = self.food_pivot[3:].corr(method='spearman', min_periods=1).abs()
        corr_matrix = fc.abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
        to_drop_pair = []
        for food_col in to_drop:
            food_col_pair = upper.idxmax()[food_col]
            to_drop_pair.append(food_col_pair)
        print('Columns to remove: ')
        print(to_drop, to_drop_pair)

        self.food_pivot[self.food_pivot.columns[3:]] = standard.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])
        self.food_pivot = self.food_pivot.reset_index(drop=True)
        awer=2134



    def PCA_analysis(self, method=sklearn.decomposition.PCA(2), reduced_data_dir=r'../data/processed/dataset_2d_pca.csv'):

        data_2d = method.fit_transform(self.food_pivot[self.food_pivot.columns[3:]])
        data_2d = pd.concat([self.food_pivot[['Area','Year']], pd.DataFrame(data_2d)], axis=1)
        data_2d.columns = ['Area','Year', 'x', 'y']

        self.PCAComp = pd.DataFrame(method.components_, columns=self.food_pivot.columns[3:], index=['PC-1', 'PC-2'])
        self.sortPCA = self.PCAComp.T.iloc[self.PCAComp.T.abs()["PC-1"].argsort()]
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
        pc1 = [self.PCAComp[col]["PC-1"] for col in self.PCAComp]
        pc2 = [self.PCAComp[col]["PC-2"] for col in self.PCAComp]
        name = self.PCAComp.columns
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
