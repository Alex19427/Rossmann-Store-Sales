# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:53:38 2017

@author: Alex
"""
## Import Library

import pandas as pd


## Import Data

train_set = pd.read_csv('E:/BDAP/Datasets/Rossmann/train.csv')
test_set = pd.read_csv('E:/BDAP/Datasets/Rossmann/test.csv')
store = pd.read_csv('E:/BDAP/Datasets/Rossmann/store.csv')


## Finding and handling the missing data in Store data set
store.describe()
store.head()

#### Checking for the missing Value
pd.Categorical(store['Assortment']).describe()
pd.Categorical(store['CompetitionDistance']).describe()
pd.Categorical(store['CompetitionOpenSinceMonth']).describe()
pd.Categorical(store['CompetitionOpenSinceYear']).describe()
pd.Categorical(store['Promo2']).describe()
pd.Categorical(store['Promo2SinceWeek']).describe()
pd.Categorical(store['Promo2SinceYear']).describe()
pd.Categorical(store['PromoInterval']).describe()
pd.Categorical(store['Store']).describe()
pd.Categorical(store['StoreType']).describe()


#### Handling Missing Value
store['PromoInterval'] = store['PromoInterval'].fillna(0)   
store['Promo2SinceWeek'] = store['Promo2SinceWeek'].fillna(0)
store['Promo2SinceYear'] = store['Promo2SinceYear'].fillna(0)
#### Fill the empty values for CompetitionOpenSinceMonth and CompetitionOpenSinceYear with mode.
#### And CompetitionDistance with median
store['CompetitionOpenSinceMonth'] = store['CompetitionOpenSinceMonth'].fillna(9)
store['CompetitionOpenSinceYear'] = store['CompetitionOpenSinceYear'].fillna(2013)
store['CompetitionDistance'] = store['CompetitionDistance'].fillna(2325)

#### Replacing Categorical data to Numeric data
store['PromoInterval'] = store['PromoInterval'].replace('Feb,May,Aug,Nov', 1)    
store['PromoInterval'] = store['PromoInterval'].replace('Jan,Apr,Jul,Oct', 2)    
store['PromoInterval'] = store['PromoInterval'].replace('Mar,Jun,Sept,Dec', 3) 
pd.Categorical(store['StoreType']).describe()
store['StoreType'] = store['StoreType'].replace(('a','b','c','d'),(1,2,3,4))
pd.Categorical(store['Assortment']).describe()
store['Assortment'] = store['Assortment'].replace(('a','b','c'),(1,2,3))

store.dtypes
store['CompetitionDistance'] = store['CompetitionDistance'].astype(int)
store['CompetitionOpenSinceMonth'] = store['CompetitionOpenSinceMonth'].astype(object)
store['CompetitionOpenSinceYear'] = store['CompetitionOpenSinceYear'].astype(object)
store['Promo2SinceWeek'] = store['Promo2SinceWeek'].astype(object)
store['Promo2SinceYear'] = store['Promo2SinceYear'].astype(object)

store.isnull().sum()

## Replacing Categorical data to Numeric data in Train data set
train_set.isnull().sum()
train_set.shape
pd.Categorical(train_set['StateHoliday']).describe()
train_set['StateHoliday'] = train_set['StateHoliday'].replace(('a','b','c'),(1,2,3))
train_set['StateHoliday'] = train_set['StateHoliday'].replace('0',0)
train_set.dtypes

#### Removing the store which are closed and whose sales are zero
#### As there forcasting will result to zero.
train_set= train_set.ix[~((train_set.Open==0)&(train_set.Sales==0))]

train_set.columns
train_set.head()


#### Handling mssing Value and replacing Categorical Value to numeric.

test_set.shape
test_set.head()
test_set.isnull().sum()
test_set['Open'] = test_set['Open'].fillna(1)
pd.Categorical(test_set['StateHoliday']).describe()
test_set['StateHoliday'] = test_set['StateHoliday'].replace(('0','a'),(0,1))



store.head()
train_set.head()
test_set.head()


store.to_csv('E:/BDAP/Datasets/Rossmann/store_df.csv')
train_set.to_csv('E:/BDAP/Datasets/Rossmann/Rossmann_train.csv')
test_set.to_csv('E:/BDAP/Datasets/Rossmann/Rossmann_test.csv')
