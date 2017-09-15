# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 12:45:59 2017

@author: Alex
"""

#### Import Library

#### pandas
import pandas as pd
from pandas import Series


#### Machine learning
from sklearn.linear_model import LinearRegression
from sklearn import ensemble
from xgboost import XGBRegressor

train_set = pd.read_csv('E:/BDAP/Datasets/Rossmann/Rossmann_train.csv',index_col=0)
test_set = pd.read_csv('E:/BDAP/Datasets/Rossmann/Rossmann_test.csv',index_col=0)
store = pd.read_csv('E:/BDAP/Datasets/Rossmann/store_df.csv',index_col=0)

train_set.info()
print("----------------------------")
store.info()
print("----------------------------")
test_set.info()


#### Create dummy varibales for DayOfWeek for both Train and test set

day_dummies  = pd.get_dummies(train_set['DayOfWeek'], prefix='Day')
day_dummies_test  = pd.get_dummies(test_set['DayOfWeek'],prefix='Day')


train_set = train_set.join(day_dummies)
test_set  = test_set.join(day_dummies_test)


#### Save ids of closed stores, because we will assign their sales value to 0 later(see below)
closed_store_ids = test_set["Id"][test_set["Open"] == 0].values               

#### Removing Observation were store is closed and sales is zero.                           
train_set= train_set.ix[~((train_set.Open==0)&(train_set.Sales==0))]                           
test_set= test_set.ix[~((test_set.Open==0))]
                           
train_set.drop(['DayOfWeek','Open','Customers', 'Date','Day_7'], axis=1,inplace=True)
test_set.drop(['DayOfWeek','Open', 'Date','Day_7'], axis=1,inplace=True)


#### Building the model                           
                           
rossmann_dic = dict(list(train_set.groupby('Store')))
test_dic     = dict(list(test_set.groupby('Store')))
submission   = Series()
scores       = []

for i in test_dic:
    
    # current store
    store = rossmann_dic[i]
    
    # define training and testing sets
    X_train = store.drop(["Sales","Store"],axis=1)
    Y_train = store["Sales"]
    X_test  = test_dic[i].copy()
    
    store_ids = X_test["Id"]
    X_test.drop(["Id","Store"], axis=1,inplace=True)
    
    # Linear Regression
    #lreg = LinearRegression()
    #lreg.fit(X_train, Y_train)
    #Y_pred = lreg.predict(X_test)
    #scores.append(lreg.score(X_train, Y_train))
    #0.14879
    
    clf = ensemble.GradientBoostingRegressor(n_estimators= 400, max_depth=5,min_samples_split=2,
                                                              learning_rate=0.01, loss = 'huber')
    clf.fit(X_train,Y_train)
    Y_pred = clf.predict(X_test)
    scores.append(clf.score(X_train, Y_train))
    #0.14755 - ls
    #0.13805 - huber
    
    #model = XGBRegressor(learning_rate=0.01,n_estimators=300,gamma=0.1,
    #                      scale_pos_weight=10,objective='reg:linear',base_score=0.5)
    #model.fit(X_train,Y_train)
    #Y_pred = model.predict(X_test)
    #scores.append(model.score(X_train, Y_train))
    #0.13588
    
    # append predicted values of current store to submission
    submission = submission.append(Series(Y_pred, index=store_ids))

# append rows(store,date) that were closed, and assign their sales value to 0
submission = submission.append(Series(0, index=closed_store_ids))

submission.to_csv('E:/BDAP/Datasets/Rossmann/submission.csv')
                          