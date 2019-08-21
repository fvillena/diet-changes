import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.preprocessing

data = pd.read_csv(
    r'../../data/raw/FoodBalanceSheets_E_All_Data_(Normalized).csv', encoding='latin-1'
    )

countries = pd.read_excel(
    r'../../data/raw/country-region.xls'
    )
countries = countries[
    countries['ISO2 Code'].isna() == False
    ][
        'Country Code'
        ].tolist()

food_information = data[
    data['Element Code'].isin([5301,511])
][
    data['Area Code'].isin(countries)
]

food_information = food_information[[
    'Area', 
    'Item', 
    'Year Code', 
    'Value'
    ]]

food_information_pivot = pd.pivot_table(
    food_information, 
    values='Value', 
    index=[
        'Area', 
        'Year Code'
        ], 
    columns=[
        'Item'
        ]
    ).reset_index()

food_information_pivot = food_information_pivot[
    food_information_pivot.columns[
        food_information_pivot.isna().sum()
        / food_information_pivot.shape[0] 
        < 0.05
        ]
    ]

food_information_pivot.sort_values(
    by=[
        'Area', 
        'Year Code'
        ], 
    inplace=True
    )
food_information_pivot.fillna(
    method='backfill', 
    inplace=True
    )

food_information_pivot[food_information_pivot.columns[2:]] = food_information_pivot[
    food_information_pivot.columns[2:]
    ].divide(
        food_information_pivot.Population, 
        axis=0
        )

food_information_pivot.drop(
    columns ='Population', 
    inplace=True
    )

standardizer = sklearn.preprocessing.StandardScaler()
food_information_pivot[food_information_pivot.columns[2:]] = standardizer.fit_transform(
    food_information_pivot[
        food_information_pivot.columns[2:]
        ]
    )

food_information_pivot = food_information_pivot.dropna()

food_information_pivot.to_csv(
    r'../../data/processed/dataset.csv',
    index=False
)