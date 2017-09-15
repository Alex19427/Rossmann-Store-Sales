# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:06:13 2017

@author: Alex
"""

#### Import Library

#### pandas
import pandas as pd

#### numpy, matplotlib, seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
 

rossmann_df = pd.read_csv('E:/BDAP/Datasets/Rossmann/Rossmann_train.csv',index_col=0)
test_df = pd.read_csv('E:/BDAP/Datasets/Rossmann/Rossmann_test.csv',index_col=0)
store_df = pd.read_csv('E:/BDAP/Datasets/Rossmann/store_df.csv',index_col=0)


rossmann_df.info()
print("----------------------------")
store_df.info()
print("----------------------------")
test_df.info()



#### Date

#### Create Year and Month columns
rossmann_df['Year']  = rossmann_df['Date'].apply(lambda x: int(str(x)[:4]))
rossmann_df['Month'] = rossmann_df['Date'].apply(lambda x: int(str(x)[5:7]))

test_df['Year']  = test_df['Date'].apply(lambda x: int(str(x)[:4]))
test_df['Month'] = test_df['Date'].apply(lambda x: int(str(x)[5:7]))

#### Assign Date column to Date(Year-Month) instead of (Year-Month-Day)
#### this column will be useful in analysis and visualization

rossmann_df['Date'] = rossmann_df['Date'].apply(lambda x: (str(x)[:7]))
test_df['Date']     = test_df['Date'].apply(lambda x: (str(x)[:7]))

#### group by date and get average sales, and precent change
average_sales    = rossmann_df.groupby('Date')["Sales"].mean()
pct_change_sales = rossmann_df.groupby('Date')["Sales"].sum().pct_change()



#### Plot the average sales and Percent change
fig, (axis1,axis2) = plt.subplots(2,1,sharex=True,figsize=(15,8))
# plot average sales over time(year-month)
ax1 = average_sales.plot(legend=True,ax=axis1,marker='o',title="Average Sales")
ax1.set_xticks(range(len(average_sales)))
ax1.set_xticklabels(average_sales.index.tolist(), rotation=90)
# plot precent change for sales over time(year-month)
ax2 = pct_change_sales.plot(legend=True,ax=axis2,marker='o',rot=90,colormap="summer",title="Sales Percent Change")


# Plot average sales & customers for every year
fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,4))
sns.barplot(x='Year', y='Sales', data=rossmann_df, ax=axis1)
sns.barplot(x='Year', y='Customers', data=rossmann_df, ax=axis2)


#### Customers

fig, (axis1,axis2) = plt.subplots(2,1,figsize=(15,8))
#### Plot max, min values, & 2nd, 3rd quartile
sns.boxplot([rossmann_df["Customers"]], whis=np.inf, ax=axis1)
#### group by date and get average customers, and precent change
average_customers      = rossmann_df.groupby('Date')["Customers"].mean()
pct_change_customers = rossmann_df.groupby('Date')["Customers"].sum().pct_change()
#### Plot average customers over the time
#### it should be correlated with the average sales over time
ax = average_customers.plot(legend=True,marker='o', ax=axis2)
ax.set_xticks(range(len(average_customers)))
xlabels = ax.set_xticklabels(average_customers.index.tolist(), rotation=90)


#### DayOfWeek

#### In both cases where the store is closed and opened
fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,4))
sns.barplot(x='DayOfWeek', y='Sales', data=rossmann_df, order=[1,2,3,4,5,6,7], ax=axis1)
sns.barplot(x='DayOfWeek', y='Customers', data=rossmann_df, order=[1,2,3,4,5,6,7], ax=axis2)


#### Sales

fig, (axis1,axis2) = plt.subplots(2,1,figsize=(15,8))
#### Plot max, min values, & 2nd, 3rd quartile
sns.boxplot([rossmann_df["Customers"]], whis=np.inf, ax=axis1)
#### Plot sales values 
rossmann_df["Sales"].plot(kind='hist',bins=70,xlim=(0,15000),ax=axis2)



#### Using store_df

#### Merge store_df with average store sales & customers
average_sales_customers = rossmann_df.groupby('Store')[["Sales", "Customers"]].mean()
sales_customers_df = pd.DataFrame({'Store':average_sales_customers.index,
                      'Sales':average_sales_customers["Sales"], 'Customers': average_sales_customers["Customers"]}, 
                      columns=['Store', 'Sales', 'Customers'])
store_df = pd.merge(sales_customers_df, store_df, on='Store')


#### StoreType 

#### Plot StoreType, & StoreType Vs average sales and customers
sns.countplot(x='StoreType', data=store_df, order=[1,2,3, 4])
fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,4))
sns.barplot(x='StoreType', y='Sales', data=store_df, order=[1,2,3, 4],ax=axis1)
sns.barplot(x='StoreType', y='Customers', data=store_df, order=[1,2,3, 4], ax=axis2)















